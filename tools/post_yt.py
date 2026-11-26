#!/usr/bin/env python3
"""Ayurveda Ka Sach Uploader - upload clips (already on IG) to our own YouTube channel as Shorts.
Uses YouTube Data API v3 videos.insert (resumable upload). Only for the channel owner's own videos.
Disabled until /opt/aks/.yt_enabled exists (sources/YT_ENABLE.md). The flag file holds the ISO time posting was
turned on: reels posted to IG from then on are "daily" (cron slots, priority); older ones are the backfill.

  post_yt.py              daily: upload the next new IG reel without a YouTube id (6 cron slots/day)
  post_yt.py --backfill   backfill (sources/YT_ENABLE.md 3): oldest-first upload of pre-enable IG reels, only as many
                          as the remaining daily quota allows after reserving the rest of today's daily slots; removes
                          its own cron line once the backlog is empty.
Quota (sources/YT_QUOTA_FIX.md): videos.insert uses its own "Video Uploads per day" bucket (100/day, 1 per upload);
other calls (videos.update, thumbnails.set, playlistItems.insert = 50, list = 1) use the 10,000 units/day bucket.
Safety margins: max 90 uploads/day, max 8,000 units/day. Both reset at midnight Pacific. Every attempt is charged in LEDGER.
On quotaExceeded / uploadLimitExceeded: stop, leave the clip untouched, retry next run.

  post_yt.py --seo-update  YT_SEO.md: apply sources/yt_seo_backfill.json to the already-uploaded videos (videos.update,
                           Hindi SRT captions, topic playlist, comment), then any pending SEO steps. Idempotent.
SEO (sources/YT_SEO.md, tools/yt_seo.py): new uploads get keyword-validated title/description/tags/localizations in
videos.insert, then captions (400 units), playlist (50) and a comment (50). Those steps need the youtube.force-ssl
scope; without it they stay pending in queue.json (yt_seo_done) and are retried every run."""
import json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
sys.path.insert(0, "/opt/aks/app")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_ig as P
import yt_seo as S

ENABLED_FLAG = "/opt/aks/.yt_enabled"
TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
MAX_UPLOADS, MAX_UNITS = 90, 8000              # safety margins under 100 uploads/day and 10,000 units/day
UPLOAD_GAP = 150                               # seconds between backfill uploads (per-minute limits)
LEDGER = "/opt/aks/logs/yt_quota.log"            # "<iso utc> <bucket: uploads|units> <amount> <clip id> <result>"
PT = ZoneInfo("America/Los_Angeles")
DAILY_SLOTS_UTC = [(2, 50), (5, 20), (7, 20), (12, 50), (15, 20), (16, 50)]  # daily post_yt.py cron lines
CORRECTIONS = "/opt/aks/assets/sources/ig_caption_corrections.md"
BACKFILL_TAG = "post_yt.py --backfill"
SEO_BACKFILL = "/opt/aks/assets/sources/yt_seo_backfill.json"
COST = {"update": 50, "captions": 400, "playlist": 50, "comment": 50}  # units bucket (YT_SEO.md 8)
NEW_STEPS, BACKFILL_STEPS = ["captions", "playlist", "comment"], ["update", "captions", "playlist", "comment"]


class QuotaExceeded(Exception):
    pass


def access_token(e):
    data = urllib.parse.urlencode({"client_id": e["YT_CLIENT_ID"], "client_secret": e["YT_CLIENT_SECRET"],
                                   "refresh_token": e["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=data), timeout=60))["access_token"]


def _open(req, timeout):
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as ex:
        body = ex.read().decode(errors="replace")[:600]
        if "quotaExceeded" in body or "uploadLimitExceeded" in body:
            raise QuotaExceeded(body)
        raise RuntimeError(f"{ex.code} {body}")


def upload(tok, path, title, desc, snippet=None, localizations=None, notify=True):
    # API uploads are not private by default: privacyStatus is always set explicitly to public.
    meta = {"snippet": snippet or {"title": title, "description": desc, "categoryId": "27",
                                   "tags": ["Ayurveda", "आयुर्वेद", "Acharya Manish Ji", "Shorts", "health"],
                                   "defaultLanguage": "hi", "defaultAudioLanguage": "hi"},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    url = UPLOAD_URL + f"&notifySubscribers={'true' if notify else 'false'}"
    if localizations:
        meta["localizations"] = localizations
        url = url.replace("part=snippet,status", "part=snippet,status,localizations")
    size = os.path.getsize(path)
    r = urllib.request.Request(url, data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = _open(r, 60).headers["Location"]
    with open(path, "rb") as f:
        r2 = urllib.request.Request(loc, data=f.read(), method="PUT",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
        return json.load(_open(r2, 600))


# ---- quota bookkeeping ----
def pt_day_bounds(now):
    p = now.astimezone(PT)
    start = p.replace(hour=0, minute=0, second=0, microsecond=0)
    return start.astimezone(timezone.utc), (start + timedelta(days=1)).astimezone(timezone.utc)


def used_today(now, bucket="uploads"):
    start, _ = pt_day_bounds(now)
    used = 0
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            f = line.split()
            if len(f) >= 3 and f[1] == bucket and datetime.fromisoformat(f[0]) >= start:
                used += int(f[2])
    return used


def charge(clip_id, result, bucket="uploads", amount=1):
    """uploads: 1 per videos.insert attempt. units: 50 per update/thumbnail/playlist call, 1 per list call."""
    with open(LEDGER, "a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} {bucket} {amount} {clip_id} {result}\n")


def daily_slots_left(now):
    _, end = pt_day_bounds(now)
    n, d = 0, now.date() - timedelta(days=1)
    while d <= end.date():
        for h, m in DAILY_SLOTS_UTC:
            t = datetime(d.year, d.month, d.day, h, m, tzinfo=timezone.utc)
            if now < t < end:
                n += 1
        d += timedelta(days=1)
    return n


# ---- clip selection ----
def enabled_since():
    try:
        return datetime.fromisoformat(open(ENABLED_FLAG).read().strip())
    except ValueError:
        return datetime.fromtimestamp(os.path.getmtime(ENABLED_FLAG), timezone.utc)


def _eligible(c):
    return (c.get("status") == "posted_ig" and not c.get("yt_video_id") and c.get("yt_status") != "failed"
            and c.get("qc", "pass") == "pass" and c.get("posted_ig_at"))


def is_backlog(c, since):
    return _eligible(c) and datetime.fromisoformat(c["posted_ig_at"]) < since


def is_daily(c, since):
    return _eligible(c) and datetime.fromisoformat(c["posted_ig_at"]) >= since


# ---- YT formatting for the backfill (same captions as posted, corrected versions) ----
def corrected_captions():
    out = {}
    if os.path.exists(CORRECTIONS):
        for title, body in re.findall(r"^## (.+?)\n.*?```\n(.*?)\n```", open(CORRECTIONS, encoding="utf-8").read(), re.S | re.M):
            out[title.strip()] = body
    return out


def yt_format(cap):
    """title <= 100 chars (Hindi title line); description = caption body + 🎥 credit + ⚠️ disclaimer + hashtags + #Shorts."""
    lines = cap.strip().splitlines()
    title = re.sub(r"[<>]", "", lines[0].strip())[:100]
    ci = next(i for i, l in enumerate(lines) if l.strip().startswith("🎥"))
    body = "\n".join(lines[1:ci]).strip()
    tags = next((l.strip() for l in reversed(lines) if l.strip().startswith("#")), "")
    if "#shorts" not in tags.lower():
        tags = (tags + " #Shorts").strip()
    # RULES_V2 4 (26 Nov 2026): keep the ⚠️ disclaimer line in YT descriptions too
    disc = next((l.strip() for l in lines[ci + 1:] if l.strip().startswith("⚠️")), P.DISCLAIMER)
    return title, f"{body}\n\n{lines[ci].strip()}\n{disc}\n\n{tags}"


def save(q, msg):
    json.dump(q, open(P.QUEUE, "w"), ensure_ascii=False, indent=2)
    P.git("add", "queue.json"); P.git("commit", "-qm", msg); P.git("push", "-q")


def remove_backfill_cron():
    cur = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    new = "".join(l + "\n" for l in cur.splitlines() if BACKFILL_TAG not in l)
    if new != cur:
        subprocess.run(["crontab", "-"], input=new, text=True, check=True)
        print("Backlog empty: backfill cron removed.")


def daily():
    since = enabled_since()
    e = P.env()
    P.git("pull", "--rebase", "-q")
    q = json.load(open(P.QUEUE))
    clip = next((c for c in q if is_daily(c, since)), None)
    if not clip:
        print("No clip for YouTube."); seo_pending(e, q); return
    now = datetime.now(timezone.utc)
    if used_today(now) + 1 > MAX_UPLOADS:
        print("YT upload budget for today used up; retry next run.", clip["id"]); return
    desc = P.build_caption(clip)
    if any(re.search(p, desc, re.I) for p in P.BANNED):
        clip["status"] = "needs_review"; print("Compliance block:", clip["id"])
    else:
        title = (clip.get("title") or clip.get("topic") or "Ayurveda Ka Sach").strip()
        title = (title[:88] + " #Shorts") if "#shorts" not in title.lower() else title[:100]
        path = os.path.join(P.A, "assets", clip["file"])
        seo = clip.get("yt_seo") or S.generate(clip)
        if seo and S.problems(clip, seo):
            print("YT SEO checks failed, plain metadata:", clip["id"], S.problems(clip, seo)); seo = None
        if seo:
            clip.update(yt_seo=seo, yt_title=seo["title"], yt_tags=S.tags(seo), yt_seo_steps=NEW_STEPS, yt_seo_done=[])
        else:
            clip["yt_seo_status"] = "fallback (generation failed)"
        try:
            v = upload(access_token(e), path, title, S.with_long_link(desc, clip), S.snippet(seo, clip) if seo else None,
                       S.localizations(seo) if seo else None, notify=True)
            charge(clip["id"], "ok " + v["id"])
            clip["yt_video_id"] = v["id"]
            clip["posted_yt_at"] = datetime.now(timezone.utc).isoformat()
            print("Posted YT", clip["id"], v["id"], v.get("status", {}).get("privacyStatus"))
        except QuotaExceeded as ex:
            charge(clip["id"], "quotaExceeded"); print("YT quota exceeded; retry next run.", clip["id"], ex); return
        except Exception as ex:
            charge(clip["id"], "failed")
            clip["yt_status"] = "failed"; print("YT failed", clip["id"], ex)
    save(q, f"yt {clip['id']}")
    seo_pending(e, q)


def backfill():
    since = enabled_since()
    e = P.env()
    P.git("pull", "--rebase", "-q")
    q = json.load(open(P.QUEUE))
    todo = sorted((c for c in q if is_backlog(c, since)), key=lambda c: c["posted_ig_at"])
    if not todo:
        remove_backfill_cron(); return
    now = datetime.now(timezone.utc)
    reserve = daily_slots_left(now)  # keep room for today's remaining daily reels
    allowed = max(0, MAX_UPLOADS - used_today(now) - reserve)
    print(f"YT backfill: backlog {len(todo)}, uploads today {used_today(now)}, reserved {reserve} daily, allowed {allowed}")
    fixed, tok = corrected_captions(), None
    for i, clip in enumerate(todo[:allowed]):
        if i:
            time.sleep(UPLOAD_GAP)
        cap = fixed.get(clip.get("title", "").strip()) or P.build_caption(clip)
        title, desc = yt_format(cap)
        if P.caption_problems(desc) or P.caption_problems(title):
            clip["status"] = "needs_review"; print("Compliance block:", clip["id"], P.caption_problems(desc + title))
            save(q, f"yt backfill {clip['id']} needs_review"); continue
        try:
            tok = tok or access_token(e)
            v = upload(tok, os.path.join(P.A, "assets", clip["file"]), title, desc)
            charge(clip["id"], "ok " + v["id"])
            clip["yt_video_id"] = v["id"]
            clip["posted_yt_at"] = datetime.now(timezone.utc).isoformat()
            print("Posted YT (backfill)", clip["id"], v["id"], v.get("status", {}).get("privacyStatus"))
        except QuotaExceeded as ex:
            charge(clip["id"], "quotaExceeded"); print("YT quota exceeded; stop, retry tomorrow.", ex); break
        except Exception as ex:
            charge(clip["id"], "failed")
            clip["yt_status"] = "failed"; print("YT failed", clip["id"], ex)
        save(q, f"yt backfill {clip['id']}")
    if not any(is_backlog(c, since) for c in q):
        remove_backfill_cron()


# ---- SEO steps after upload (YT_SEO.md 4-8) ----
def _units_ok(cost):
    return used_today(datetime.now(timezone.utc), "units") + cost <= MAX_UNITS


def seo_pending(e, q, only=None):
    """Run outstanding SEO steps (update/captions/playlist/comment) for uploaded clips. Saves after every step."""
    todo = [c for c in q if c.get("yt_video_id") and c.get("yt_seo") and (only is None or c["id"] in only)
            and set(c.get("yt_seo_steps", [])) - set(c.get("yt_seo_done", []))]
    if not todo:
        return []
    tok = access_token(e)
    if not S.has_force_ssl(tok):
        print(f"YT SEO: {len(todo)} video(s) waiting: token lacks youtube.force-ssl scope (run tools/yt_auth.py).")
        return []
    pls, done_ids = None, []
    for i, c in enumerate(todo):
        seo, vid, done = c["yt_seo"], c["yt_video_id"], c.setdefault("yt_seo_done", [])
        for step in [s for s in c["yt_seo_steps"] if s not in done]:
            if not _units_ok(COST[step] + (251 if step == "playlist" and pls is None else 0)):
                print("YT SEO: unit budget for today used; rest tomorrow.", c["id"], step); save(q, "yt seo partial"); return done_ids
            try:
                if step == "update":
                    S.videos_update(sys.modules[__name__], tok, vid, c, seo)
                elif step == "captions":
                    S.captions_insert(sys.modules[__name__], tok, vid, c)
                elif step == "playlist":
                    pls = pls or S.playlists(sys.modules[__name__], tok, lambda cid, res, n: charge(cid, res, "units", n))
                    S.playlist_add(sys.modules[__name__], tok, pls[seo["playlist"]], vid)
                elif step == "comment":
                    S.comment(sys.modules[__name__], tok, e["YT_CHANNEL_ID"], vid, seo["comment"])
                charge(c["id"], f"ok {step} {vid}", "units", COST[step])
                done.append(step)
            except QuotaExceeded as ex:
                charge(c["id"], f"quotaExceeded {step}", "units", COST[step])
                print("YT quota exceeded during SEO; retry next run.", ex); save(q, "yt seo partial"); return done_ids
            except Exception as ex:
                charge(c["id"], f"failed {step}", "units", COST[step])
                c.setdefault("yt_seo_errors", {})[step] = str(ex)[:300]
                print("YT SEO step failed", c["id"], step, ex)
                if step == "update":
                    break  # don't add captions/playlist/comment to a video whose metadata failed
        c["yt_seo_status"] = "done" if set(c["yt_seo_steps"]) <= set(done) else "partial: " + ",".join(done)
        S.log(c, seo, {s: (s in done) for s in c["yt_seo_steps"]})
        save(q, f"yt seo {c['id']}")
        done_ids.append(c["id"])
    return done_ids


def seo_update():
    """YT_SEO.md: metadata update for the videos uploaded before SEO was on (notifySubscribers false: update only)."""
    e = P.env()
    P.git("pull", "--rebase", "-q")
    q = json.load(open(P.QUEUE))
    data = {k: v for k, v in json.load(open(SEO_BACKFILL, encoding="utf-8")).items() if not k.startswith("_")}
    byid = {c["id"]: c for c in q}
    for cid, seo in data.items():
        c = byid[cid]
        if c.get("yt_video_id") != seo["video_id"]:
            raise SystemExit(f"{cid}: queue has {c.get('yt_video_id')}, backfill file says {seo['video_id']}")
        pr = S.problems(c, seo)
        if pr:
            raise SystemExit(f"{cid}: SEO checks failed: {pr}")
        if c.get("yt_seo") != seo:
            c.update(yt_seo=seo, yt_title=seo["title"], yt_tags=S.tags(seo), yt_seo_steps=BACKFILL_STEPS,
                     yt_seo_done=[s for s in c.get("yt_seo_done", []) if s != "update"])
    save(q, "yt seo backfill metadata")
    seo_pending(e, q)
    q = json.load(open(P.QUEUE))
    for c in q:
        if c["id"] in data:
            print(c["id"], c["yt_video_id"], c.get("yt_seo_status"), "|", c["yt_title"])
    ok = [c["yt_title"] for c in q if c["id"] in data and c.get("yt_seo_status") == "done"]
    if len(ok) == len(data):
        print("YT SEO ON:", " / ".join(ok))
    else:
        print(f"YT SEO pending: {len(ok)}/{len(data)} videos updated; the rest retry on the next post_yt.py run.")


def main():
    if not os.path.exists(ENABLED_FLAG):
        print("YouTube posting disabled (waiting for API audit)."); return
    if "--seo-update" in sys.argv:
        seo_update()
    else:
        backfill() if "--backfill" in sys.argv else daily()


if __name__ == "__main__":
    main()
