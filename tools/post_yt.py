#!/usr/bin/env python3
"""Ayurveda Ka Sach Uploader - upload the next clip (already on IG) to our own YouTube channel as a Short.
Uses YouTube Data API v3 videos.insert (resumable upload). Only for the channel owner's own videos.
Disabled until /opt/aks/.yt_enabled exists (create it only after the YouTube API compliance audit passes)."""
import json, os, re, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/aks/app")
import post_ig as P

ENABLED_FLAG = "/opt/aks/.yt_enabled"
TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

def access_token(e):
    data = urllib.parse.urlencode({"client_id": e["YT_CLIENT_ID"], "client_secret": e["YT_CLIENT_SECRET"],
                                   "refresh_token": e["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=data), timeout=60))["access_token"]

def upload(tok, path, title, desc):
    meta = {"snippet": {"title": title, "description": desc, "categoryId": "27",
                        "tags": ["Ayurveda", "आयुर्वेद", "Acharya Manish Ji", "Shorts", "health"],
                        "defaultLanguage": "hi", "defaultAudioLanguage": "hi"},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    size = os.path.getsize(path)
    r = urllib.request.Request(UPLOAD_URL, data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = urllib.request.urlopen(r, timeout=60).headers["Location"]
    with open(path, "rb") as f:
        r2 = urllib.request.Request(loc, data=f.read(), method="PUT",
            headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
        return json.load(urllib.request.urlopen(r2, timeout=600))

def main():
    if not os.path.exists(ENABLED_FLAG):
        print("YouTube posting disabled (waiting for API audit)."); return
    e = P.env()
    P.git("pull", "--rebase", "-q")
    q = json.load(open(P.QUEUE))
    clip = next((c for c in q if c.get("status") == "posted_ig" and not c.get("yt_video_id")
                 and c.get("yt_status") != "failed"), None)
    if not clip:
        print("No clip for YouTube."); return
    desc = P.build_caption(clip)
    if any(re.search(p, desc, re.I) for p in P.BANNED):
        clip["status"] = "needs_review"; print("Compliance block:", clip["id"])
    else:
        title = (clip.get("title") or clip.get("topic") or "Ayurveda Ka Sach").strip()
        title = (title[:88] + " #Shorts") if "#shorts" not in title.lower() else title[:100]
        path = os.path.join(P.A, "assets", clip["file"])
        try:
            v = upload(access_token(e), path, title, desc)
            clip["yt_video_id"] = v["id"]
            clip["posted_yt_at"] = datetime.now(timezone.utc).isoformat()
            print("Posted YT", clip["id"], v["id"], v.get("status", {}).get("privacyStatus"))
        except Exception as ex:
            clip["yt_status"] = "failed"; print("YT failed", clip["id"], ex)
    json.dump(q, open(P.QUEUE, "w"), ensure_ascii=False, indent=2)
    P.git("add", "queue.json"); P.git("commit", "-qm", f"yt {clip['id']}"); P.git("push", "-q")

if __name__ == "__main__":
    main()