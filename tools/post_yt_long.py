#!/opt/aks/venv/bin/python
"""YT_LONG.md: upload the long video built for today (Tue/Fri 19:00 IST cron), YouTube only, public.

  post_yt_long.py            upload today's ready long video (work/long/<LID>, report status "ready", post_date = today IST)
  post_yt_long.py --pending  retry outstanding steps (thumbnail, captions, playlist, comment) of uploaded long videos

Quota (YT_QUOTA_FIX.md, same ledger as post_yt.py): upload = 1 in the uploads bucket; thumbnails.set 50, captions 400,
playlist 50, comment 50 units. captions/playlist/comment need the youtube.force-ssl scope; without it they stay pending.
Thumbnail: if the channel is not verified for custom thumbnails, it is logged and skipped.
After upload: the next (up to) 3 Shorts on the same topic (meta.json "link_shorts") get "पूरा वीडियो: <url>" in their
YouTube description (post_yt.py / yt_seo.snippet read clip["yt_long_url"])."""
import hashlib, json, os, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0, "/opt/aks/app"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_ig as P
import post_yt as Y
import yt_seo as S
import long_build as L

LONG = Path("/opt/aks/work/long")
LQ = Path("/opt/aks/assets/long_queue.json")      # uploaded long videos + pending steps (committed)
COST = {"thumbnail": 50, "captions": 400, "playlist": 50, "comment": 50}
STEPS = ["thumbnail", "captions", "playlist", "comment"]
IST = ZoneInfo("Asia/Kolkata")


def lq():
    return json.load(open(LQ)) if LQ.exists() else []


def save_lq(items, msg):
    json.dump(items, open(LQ, "w"), ensure_ascii=False, indent=2)
    P.git("add", "long_queue.json", "sources/long_log.md", "sources/long_plan.md"); P.git("commit", "-qm", msg); P.git("push", "-q")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def thumbnail(tok, vid, path):
    r = urllib.request.Request(f"{S.UPLOAD_API}/thumbnails/set?videoId={vid}", data=open(path, "rb").read(), method="POST",
                               headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
    return json.load(Y._open(r, 120))


def captions(tok, vid, srt_text):
    b = "aksLONGboundary"
    meta = {"snippet": {"videoId": vid, "language": "hi", "name": "Hindi", "isDraft": False}}
    data = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt_text.encode("utf-8") + f"\r\n--{b}--\r\n".encode()
    return S._req(Y, tok, "POST", f"{S.UPLOAD_API}/captions?part=snippet&uploadType=multipart", data=data,
                  headers={"Content-Type": f"multipart/related; boundary={b}"})


def pending(e, items):
    todo = [x for x in items if x.get("yt_video_id") and set(STEPS) - set(x.get("done", []))]
    if not todo:
        return
    tok = Y.access_token(e)
    force = S.has_force_ssl(tok)
    pls = None
    for x in todo:
        d, vid, done = Path(x["dir"]), x["yt_video_id"], x.setdefault("done", [])
        m = json.loads((d / "meta.json").read_text())
        for step in [s for s in STEPS if s not in done]:
            if step != "thumbnail" and not force:
                print(f"YT LONG {x['id']}: {step} waiting: token lacks youtube.force-ssl scope (run tools/yt_auth.py)."); continue
            if not Y._units_ok(COST[step] + (251 if step == "playlist" and pls is None else 0)):
                print("YT LONG: unit budget for today used; rest tomorrow.", x["id"], step); break
            try:
                if step == "thumbnail":
                    thumbnail(tok, vid, d / "thumb.jpg")
                elif step == "captions":
                    captions(tok, vid, (d / "final.srt").read_text(encoding="utf-8"))
                elif step == "playlist":
                    pls = pls or S.playlists(Y, tok, lambda cid, res, n: Y.charge(cid, res, "units", n))
                    S.playlist_add(Y, tok, pls[m["playlist"]], vid)
                elif step == "comment":
                    S.comment(Y, tok, e["YT_CHANNEL_ID"], vid, m["comment"])
                Y.charge(x["id"], f"ok {step} {vid}", "units", COST[step]); done.append(step)
            except Y.QuotaExceeded as ex:
                Y.charge(x["id"], f"quotaExceeded {step}", "units", COST[step]); print("YT quota exceeded; retry later.", ex); break
            except Exception as ex:
                Y.charge(x["id"], f"failed {step}", "units", COST[step])
                x.setdefault("errors", {})[step] = str(ex)[:300]
                if step == "thumbnail" and "403" in str(ex):
                    done.append(step); x["thumbnail_note"] = "channel not verified for custom thumbnails: skipped"
                    print("YT LONG thumbnail skipped (channel not verified for custom thumbnails):", x["id"])
                else:
                    print("YT LONG step failed", x["id"], step, ex)
        save_lq(items, f"yt long steps {x['id']}")


def link_shorts(ids, url):
    q = json.load(open(P.QUEUE)); n = 0
    for c in q:
        if c["id"] in ids and not c.get("yt_video_id") and not c.get("yt_long_url"):
            c["yt_long_url"] = url; n += 1
    Y.save(q, f"link {n} shorts to long video")
    return n


def upload_today(e):
    today = datetime.now(IST).date().isoformat()
    cands = [d for d in sorted(LONG.glob("*")) if (d / "plan.json").exists() and (d / "report.json").exists()
             and json.loads((d / "plan.json").read_text()).get("post_date") == today]
    if any(x.get("post_date") == today for x in lq()):
        print("YT LONG: already uploaded for", today); return
    ready = [d for d in cands if json.loads((d / "report.json").read_text()).get("status") == "ready"]
    if not ready:
        print("YT LONG: no ready long video for", today, "(nothing posted)")
        L.log_md(f"## {today}: no long video posted\n- reason: no ready build in work/long for this date"); save_lq(lq(), f"yt long none {today}")
        return
    d = ready[0]; plan = json.loads((d / "plan.json").read_text()); rep = json.loads((d / "report.json").read_text())
    m = json.loads((d / "meta.json").read_text()); final = d / f"{rep['id']}_final.mp4"
    if rep.get("semantic_check") != "pass" or rep.get("sha256") != sha(final):
        L.reject(d, "final video not approved or changed after approval"); save_lq(lq(), f"yt long reject {rep['id']}"); return
    desc = (d / "description.txt").read_text(encoding="utf-8")
    if P.caption_problems(desc + m["title"]):
        L.reject(d, f"metadata compliance {P.caption_problems(desc + m['title'])}"); save_lq(lq(), f"yt long reject {rep['id']}"); return
    if Y.used_today(datetime.now(timezone.utc)) + 1 > Y.MAX_UPLOADS:
        print("YT upload budget for today used up; long video not posted.", rep["id"]); return
    snip = {"title": m["title"], "description": desc, "tags": m["tags"], "categoryId": "27",
            "defaultLanguage": "hi", "defaultAudioLanguage": "hi"}
    try:
        v = Y.upload(Y.access_token(e), str(final), m["title"], desc, snip, None, notify=True)
    except Y.QuotaExceeded as ex:
        Y.charge(rep["id"], "quotaExceeded"); print("YT quota exceeded; long video not posted.", ex); return
    except Exception as ex:
        Y.charge(rep["id"], "failed"); print("YT LONG upload failed", rep["id"], ex); return
    vid = v["id"]; url = f"https://www.youtube.com/watch?v={vid}"
    Y.charge(rep["id"], "ok " + vid)
    print("Posted YT LONG", rep["id"], vid, v.get("status", {}).get("privacyStatus"))
    n = link_shorts(m.get("link_shorts", [])[:3], url)
    segs = "\n".join(f"  - {s['video_id']} {L.hms(float(s['offset']) + float(s['start']))}-{L.hms(float(s['offset']) + float(s['end']))}"
                     + (f" (cuts {s['cuts']})" if s.get("cuts") else "") + f" · {s['chapter']}" for s in plan["segments"])
    L.log_md(f"## {rep['id']} posted {today} 19:00 IST\n- topic: {plan['topic']}\n- format: {plan['format']}\n"
             f"- title: {m['title']}\n- duration: {L.hms(rep['duration'])} ({rep['duration']:.0f} s)\n- URL: {url}\n"
             f"- segments (source id + original timestamps):\n{segs}\n- shorts linked: {n}\n- Shorts reuse: {rep['shorts_reuse']['ratio']:.0%}")
    items = lq()
    items.append({"id": rep["id"], "post_date": today, "dir": str(d), "yt_video_id": vid, "url": url,
                  "posted_at": datetime.now(timezone.utc).isoformat(), "done": []})
    save_lq(items, f"yt long {rep['id']} {vid}")
    pending(e, items)


def main():
    if not os.path.exists(Y.ENABLED_FLAG):
        print("YouTube posting disabled (waiting for API audit)."); return
    e = P.env()
    P.git("pull", "--rebase", "-q")
    if "--pending" in sys.argv:
        pending(e, lq())
    else:
        upload_today(e)


if __name__ == "__main__":
    main()
