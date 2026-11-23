# YouTube quota correction (user approved, 24 Nov 00:20 IST)

The 1,600-units-per-upload assumption in YT_ENABLE.md is outdated. Current YouTube Data API quota (developers.google.com/youtube/v3/determine_quota_cost, and confirmed on this project's Cloud Console quota page):
- videos.insert has its own bucket: "Video Uploads per day" = 100, each upload costs 1 from that bucket (not from the 10,000 units).
- Other calls (videos.update, thumbnails.set, playlistItems.insert = 50 each; list calls = 1) still use the 10,000 units/day bucket.

Fix:
1. Update the quota ledger / post_yt.py logic: count uploads against a 100/day uploads budget and other calls against 10,000 units. Keep a safety margin (max 90 uploads/day total, max 8,000 units/day).
2. Backfill: no longer needs to wait. Upload the whole backlog of reels already posted on IG/FB (oldest first) now, spaced 2-3 minutes apart (per-minute limits), within the margins above, then remove the backfill cron. Same caption/title/public rules as YT_ENABLE.md; set privacyStatus "public" explicitly.
3. Daily reels keep posting to YouTube as normal.
4. Commit tools/ and sources/ changes, push. Print one line: YT QUOTA FIXED, with the number of backlog videos uploaded and their YouTube ids in the post log.
