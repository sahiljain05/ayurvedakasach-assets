#!/usr/bin/env python3
"""Ayurveda Ka Sach Uploader - upload clips (already on IG) to our own YouTube channel as Shorts.
Uses YouTube Data API v3 videos.insert (resumable upload). Only for the channel owner's own videos.
Disabled until /opt/aks/.yt_enabled exists (sources/YT_ENABLE.md). The flag file holds the ISO time posting was
turned on: reels posted to IG from then on are "daily" (cron slots, priority); older ones are the backfill.

  post_yt.py              daily: upload the next new IG reel without a YouTube id (6 cron slots/day)
  post_yt.py --backfill   backfill (sources/YT_ENABLE.md 3): oldest-first upload of pre-enable IG reels, only as many
                          as the remaining daily quota allows after reserving the rest of today's daily slots; removes
                          its own cron line once the backlog is empty.
Quota: ~1,600 units per upload, 10,000/day, resets at midnight Pacific. Every attempt is charged in LEDGER.
On quotaExceeded / uploadLimitExceeded: stop, leave the clip untouched, retry next run."""
import json, os, re, subprocess, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
sys.path.insert(0, "/opt/aks/app")
import post_ig as P

ENABLED_FLAG = "/opt/aks/.yt_enabled"
TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
QUOTA, COST = 10000, 1600
LEDGER = "/opt/aks/logs/yt_quota.log"            # "<iso utc> <units> <clip id> <result>"
PT = ZoneInfo("America/Los_Angeles")
DAILY_SLOTS_UTC = [(2, 50), (5, 20), (7, 20), (12, 50), (15, 20), (16, 50)]  # daily post_yt.py cron lines
CORRECTIONS = "/opt/aks/assets/sources/ig_caption_corrections.md"
BACKFILL_TAG = "post_yt.py --backfill"


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


def upload(tok, path, title, desc):
    # API uploads are not private by default: privacyStatus is always set explicitly to public.
    meta = {"snippet": {"title": title, "description": desc, "categoryId": "27",
                        "tags": ["Ayurveda", "आयुर्वेद", "Acharya Manish Ji", "Shorts", "health"],
                        "defaultLanguage": "hi", "defaultAudioLanguage": "hi"},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    size = os.path.getsize(path)
    r = urllib.request.Request(UPLOAD_URL, data=json.dumps(meta).encode(), method="POST",
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


def used_today(now):
    start, _ = pt_day_bounds(now)
    used = 0
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            f = line.split()
            if len(f) >= 2 and datetime.fromisoformat(f[0]) >= start:
                used += int(f[1])
    return used


def charge(clip_id, result):
    with open(LEDGER, "a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} {COST} {clip_id} {result}\n")


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
    """title <= 100 chars (Hindi title line); description = caption body + 🎥 credit + hashtags + #Shorts."""
    lines = cap.strip().splitlines()
    title = re.sub(r"[<>]", "", lines[0].strip())[:100]
    ci = next(i for i, l in enumerate(lines) if l.strip().startswith("🎥"))
    body = "\n".join(lines[1:ci]).strip()
    tags = next((l.strip() for l in reversed(lines) if l.strip().startswith("#")), "")
    if "#shorts" not in tags.lower():
        tags = (tags + " #Shorts").strip()
    return title, f"{body}\n\n{lines[ci].strip()}\n\n{tags}"


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
        print("No clip for YouTube."); return
    now = datetime.now(timezone.utc)
    if used_today(now) + COST > QUOTA:
        print("YT quota for today used up; retry next run.", clip["id"]); return
    desc = P.build_caption(clip)
    if any(re.search(p, desc, re.I) for p in P.BANNED):
        clip["status"] = "needs_review"; print("Compliance block:", clip["id"])
    else:
        title = (clip.get("title") or clip.get("topic") or "Ayurveda Ka Sach").strip()
        title = (title[:88] + " #Shorts") if "#shorts" not in title.lower() else title[:100]
        path = os.path.join(P.A, "assets", clip["file"])
        try:
            v = upload(access_token(e), path, title, desc)
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


def backfill():
    since = enabled_since()
    e = P.env()
    P.git("pull", "--rebase", "-q")
    q = json.load(open(P.QUEUE))
    todo = sorted((c for c in q if is_backlog(c, since)), key=lambda c: c["posted_ig_at"])
    if not todo:
        remove_backfill_cron(); return
    now = datetime.now(timezone.utc)
    slots = daily_slots_left(now)
    pending = sum(1 for c in q if is_daily(c, since))
    reserve = slots if os.path.exists("/opt/aks/.autopost") else min(slots, pending)  # new daily reels first
    allowed = max(0, (QUOTA - used_today(now) - reserve * COST) // COST)
    print(f"YT backfill: backlog {len(todo)}, used today {used_today(now)}, reserved {reserve} daily, allowed {allowed}")
    fixed, tok = corrected_captions(), None
    for clip in todo[:allowed]:
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


def main():
    if not os.path.exists(ENABLED_FLAG):
        print("YouTube posting disabled (waiting for API audit)."); return
    backfill() if "--backfill" in sys.argv else daily()


if __name__ == "__main__":
    main()
