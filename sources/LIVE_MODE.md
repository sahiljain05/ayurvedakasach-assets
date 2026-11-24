# Live-stream + large-video sourcing (user approved, 25 Nov 01:10 IST)

Problem: the source pool is running dry (23 Nov nightly run added 0 clips; batch-2 videos are 1-3 min, ~1 clip each; 6 big webinars blocked by vidIQ's 299 MB import limit). Fix: use Acharya Manish Ji's long official LIVE streams and big webinars, fetched with yt-dlp in parts.

## 1. Sources
- Official channel only (@acharyamanishji), its Live/streams tab, newest first. Start with:
  pET8b5mZhCw  # "Jeena Sikho HiiMS Delhi/NCR Meerut से Acharya Manish Ji Live", 2:46:15, 21 Nov 2026
- Then the 6 webinars that were blocked by the 299 MB vidIQ limit (WEBINAR_MODE.md list).
- Keep a list in sources/live_videos.txt (id, title, length, date, status). Add up to 10 more official lives after pET8b5mZhCw.

## 2. Fetch (no vidIQ, no full-video download)
1. Captions first: yt-dlp --skip-download --write-auto-subs --sub-langs hi (fallback: audio-only m4a + Chirp on candidate windows only).
2. Pick windows from the captions (same caption-first method as WEBINAR_MODE.md).
3. Download only the chosen windows: yt-dlp --download-sections "*start-end" -f "bv*[height<=1080]+ba/b" with 3 s padding each side. Then Chirp 3 on each window only.
4. Use the repo's existing yt-dlp setup (same as the caption fetch already used). Respect YouTube rate limits: one live at a time, sleep between section downloads.

## 3. What to clip from a live
- Acharya Ji explaining a lifestyle / diet / routine / Ayurveda concept, 25-60 s, complete sentences, strong first 3 s.
- Up to 10 clips per live in total, max 3 clips from the same live per day.
- Never: patient testimonials or patients on stage (consent + outcome claims), audience Q&A about a named disease, hospital/package/price promo, phone numbers, Dr. Biswaroop Roy Chowdhury on screen or voice, crowd-only shots, any cure/disease claim (same compliance screen as all clips).
- Live streams are often wide stage shots: use the existing speaker-crop + face QC; skip windows where QC fails.
- Credit line as usual (🎥 Acharya Manish Ji, official YouTube) with the live's URL.

## 4. Keep a buffer
- Target 10+ ready clips. The nightly run keeps going through live_videos.txt until the queue has 12 ready or the sources are used up.
- Add a 07:30 IST cron check: if ready < 6, start an extra pipeline run (setsid nohup, never tied to a terminal) and write a line to logs/buffer_alert.log and review/BUFFER_ALERT.md (committed) saying how many are ready.
- All manual or extra runs: setsid nohup, so a closed SSH session cannot stop them.

## 5. Now
- Wait for tonight's running pipeline to finish (don't disturb it), then start a LIVE_MODE run in the background (setsid nohup) on pET8b5mZhCw so tomorrow has 6+ ready clips.
- Don't change posting times, posting scripts' logic (other than fixes already approved), QC or caption rules.
- Commit sources/ tools/ app/ changes you made, push. Print one line: LIVE MODE ON with the ready count.
