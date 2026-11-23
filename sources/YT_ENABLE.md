# YouTube posting ON (user approved, 23 Nov 23:50 IST)

Google completed the YouTube API Services compliance review (email 23 Nov, 11:41 PM: no further action required).

1. Turn on YouTube auto-posting: create /opt/aks/.yt_enabled (owned by aksbot). From the next run, every reel that posts to IG/FB also posts to YouTube (Shorts), public, via tools/post_yt.py.
   Note from Google: API uploads are NOT private by default, so set privacyStatus explicitly to "public" in the upload call (never rely on the default).
2. Backfill: upload to YouTube every reel already posted on Instagram/Facebook (including aks001) that has no YouTube id yet, oldest first, using the same captions as posted (corrected versions from sources/CAPTION_FIX.md and ig_caption_corrections.md), formatted for YT: title ≤ 100 chars (Hindi title line), description = caption body + 🎥 credit + hashtags + #Shorts. Record each YouTube video id in queue.json / post log.
3. Quota: one upload costs ~1,600 units of the 10,000/day project quota (resets at midnight Pacific). New daily reels have priority. Put backfill uploads in a separate cron (e.g. 13:45 IST, after Pacific reset) that uploads only as many as the remaining quota allows, until the backlog is empty, then removes itself. Never exceed quota; on a quotaExceeded error, stop and retry next day.
4. No QC-failed or needs_review clips. No Dr. Biswaroop footage. Don't change anything else in the pipeline.
5. Commit only sources/ and tools/ changes you made, push. Print one line: YT POSTING ON with the backlog count and the expected days to clear it.
