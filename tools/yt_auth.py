#!/usr/bin/env python3
"""Re-authorize the YouTube refresh token with the youtube.force-ssl scope (needed by YT_SEO.md for videos.update,
captions.insert, playlists, playlistItems and comments). Two non-interactive steps:

  yt_auth.py url              print the Google consent URL; open it, sign in as the channel owner, approve
  yt_auth.py code '<URL>'     paste the full http://localhost/?code=... URL the browser was sent to (the page itself
                              will not load; copy it from the address bar). Saves YT_REFRESH_TOKEN in /opt/aks/.meta_env
                              (backup kept) after checking the new token has upload + force-ssl scopes."""
import json, shutil, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/aks/app")
import post_ig as P

REDIRECT = "http://localhost"
CHANNEL_ID = "UCSIhwJNYD63NzxiPOT3ru7A"  # Ayurveda Ka Sach: the only channel a saved token may belong to
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    e = P.env()
    if sys.argv[1:2] == ["url"]:
        print("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
            "client_id": e["YT_CLIENT_ID"], "redirect_uri": REDIRECT, "response_type": "code", "scope": " ".join(SCOPES),
            "access_type": "offline", "prompt": "consent", "include_granted_scopes": "true"}))
        return
    if sys.argv[1:2] != ["code"] or len(sys.argv) < 3:
        raise SystemExit(__doc__)
    arg = sys.argv[2]
    code = urllib.parse.parse_qs(urllib.parse.urlparse(arg).query).get("code", [arg])[0]
    data = urllib.parse.urlencode({"code": code, "client_id": e["YT_CLIENT_ID"], "client_secret": e["YT_CLIENT_SECRET"],
                                   "redirect_uri": REDIRECT, "grant_type": "authorization_code"}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=60))
    got = set(r.get("scope", "").split())
    missing = [s for s in SCOPES[:1] + SCOPES[2:] if s not in got]
    if missing or "refresh_token" not in r:
        raise SystemExit(f"Not saved: missing {missing or 'refresh_token'} (granted: {sorted(got)})")
    # CHANNEL CHECK (user decision 25 Nov 2026): never save a token that does not see our channel. On 24 Nov a token
    # approved with the wrong Google account (no channel) replaced the working one and every YouTube write failed.
    try:
        ch = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
            headers={"Authorization": f"Bearer {r['access_token']}"}), timeout=60))
        with open("/opt/aks/logs/yt_quota.log", "a") as f:  # 1 unit, same ledger as post_yt.py
            f.write(f"{datetime.now(timezone.utc).isoformat()} units 1 yt_auth list channels.mine\n")
    except Exception as ex:
        raise SystemExit(f"Not saved: could not check which channel the token belongs to ({ex}); old token kept.")
    seen = [(i["id"], i["snippet"]["title"]) for i in ch.get("items", [])]
    if CHANNEL_ID not in [cid for cid, _ in seen]:
        raise SystemExit(f"Not saved: this token sees channel(s) {seen or 'NONE'}, not {CHANNEL_ID} (Ayurveda Ka Sach). "
                         "Sign in again with the account that manages the channel and pick Ayurveda Ka Sach in the "
                         "account/channel chooser. Old token kept.")
    print(f"Channel check OK: {seen}")
    bak =f"{P.ENV}.bak-{time.strftime('%Y-%m-%d_%H%M')}-ytauth"
    shutil.copy2(P.ENV, bak)
    lines = open(P.ENV).read().splitlines()
    lines = [f"YT_REFRESH_TOKEN={r['refresh_token']}" if l.startswith("YT_REFRESH_TOKEN=") else l for l in lines]
    open(P.ENV, "w").write("\n".join(lines) + "\n")
    print(f"Saved new YT_REFRESH_TOKEN (backup {bak}). Scopes: {sorted(got)}")


if __name__ == "__main__":
    main()
