# Bigger source pool from the official channel (user approved, 26 Nov)

Problem: 26 Nov only 1 reel posted; queue is empty. LIVE_MODE gave 4 clips from 17 lives/webinars (most were disease/patient/promo webinars, phone-number tickers, or Acharya Ji not speaking). Same compliance rules stay; we need many more clean lifestyle sources.

## 1. Build the pool (no vidIQ)
- List ALL regular uploads of the official channel @acharyamanishji (the /videos tab, not /streams, not /shorts) with yt-dlp --flat-playlist (id, title, duration, view_count, upload_date).
- Keep videos 4-45 min long whose title/description is about lifestyle, diet, dincharya, food rules, sleep, yoga/pranayam, mind/stress, seasonal routine, kitchen/home habits, Ayurveda concepts, podcasts/interviews with Acharya Ji. Drop titles that are about a named disease, cure, testimonial/patient story, hospital/centre/package, product, mantra/havan.
- Skip anything already in new_videos.txt, live_videos.txt, webinar_log.md or queue.json.
- Rank by view_count (higher first) and write the top 150 to sources/pool_videos.txt (id | title | length | views | date | status). Commit.

## 2. Process
- Caption-first (yt-dlp auto-subs hi) + --download-sections windows only, Chirp 3 only on chosen windows, same selection/compliance/QC/speaker-crop/caption rules as the rest of the pipeline. Up to 3 clips per video.
- The nightly run and the 07:30 buffer run take sources in this order: live_videos.txt todo → pool_videos.txt todo → new_videos.txt todo, until 12 ready.
- Burned-in promo ticker / phone number at the bottom of an otherwise clean window: allowed only if the reel's crop fully removes it (verify on the contact sheet). Otherwise skip, as now.

## 3. Now
- Start a run right away (setsid nohup, single-instance lock) on pool_videos.txt until 8 clips are ready, so tomorrow's 6 slots are filled. Don't disturb the 27 Nov long-video post.
- Add a line to logs and review/BUFFER_ALERT.md with the ready count when this run ends.
- Commit sources/ changes, push. Print one line: POOL READY with pool size and current ready count.
