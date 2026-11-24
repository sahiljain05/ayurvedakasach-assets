# YouTube long videos, 6-12 min (user approved, 25 Nov 01:25 IST)

User decisions: format = both (mostly topic compilations, sometimes one long segment); 2 per week; auto-post (no manual review); official channel has no Content ID; source order in live_videos.txt unchanged.

## 1. Schedule
- 2 long videos per week, YouTube only, public: Tuesday and Friday 19:00 IST (cron). Shorts keep their 6/day schedule.
- Build each long video the day before (after the nightly run, setsid nohup) so the post slot only uploads.

## 2. Formats
A. Topic compilation (default, ~3 of every 4 videos): one topic, e.g. "सुबह की दिनचर्या: आचार्य जी के 7 नियम", "खाने के 10 नियम", "रात की आदतें और नींद". 5-10 clean segments (40-120 s each) from different lives/webinars/videos, each a complete thought.
B. Single long segment (~1 of every 4): one continuous 6-12 min stretch from one live/podcast where Acharya Ji explains one lifestyle topic and passes compliance end to end.

Both formats must add original value so they are not plain re-uploads (YouTube reused-content policy):
- 4-6 s intro title card with the topic, then a 1-line text hook.
- A chapter card before each segment ("नियम 3: खाने के साथ पानी") and YouTube chapters in the description (00:00 first, ≥ 3 chapters, each ≥ 10 s).
- Burned Hindi captions (same style as reels), lower-third credit "आचार्य मनीष जी" on first appearance of each segment.
- 8-10 s outro card: summary of the points + "पूरी बात सुनें: Acharya Manish Ji official channel".
- Landscape 1920x1080 (fit + blur for non-16:9 sources), loudnorm -16 LUFS, H.264 crf 20.
- Optional short b-roll from our own assets only (no stock without licence).

## 3. Compliance (stricter, because auto-post)
- Same screen as Shorts on every segment AND on the joined transcript: no cure/disease claims, no disease names as promise, no stop-medicine hints, no patient testimonials or patients on screen, no Q&A about a named disease, no hospital/package/price/phone promo, no Dr. Biswaroop footage or voice.
- A segment must start and end on complete sentences; cut out claims inside a segment only if the cut is clean, else drop the segment.
- Chirp 3 transcript of the final joined video is re-checked before upload; if anything fails, don't post: move to work/long_review/ and log the reason.
- Face/speaker QC on every segment (no wrong speaker, no long crowd shots).
- Never reuse a segment that already went out as a Short within the last 30 days as more than 30% of a long video.

## 4. YouTube metadata (YT_SEO.md rules, long-form version)
- Title 50-70 chars, primary search phrase first (validated with YouTube autocomplete), e.g. "सुबह उठकर क्या करें? आचार्य जी के 7 नियम | Ayurveda Dincharya".
- Description: 2-line summary with the keyword, chapters, key points, credits with links to every source video used, 📚 संदर्भ only if research exists, ⚠️ disclaimer line, 3 hashtags.
- Tags, category 27, defaultLanguage/AudioLanguage hi, Hindi SRT captions upload, best-fit playlist, pinned question comment.
- Thumbnail: 1280x720 JPG, a clear frame of Acharya Ji + 3-5 big Hindi words (no claims, no disease words). Upload with thumbnails.set; if the channel isn't verified for custom thumbnails, log it and continue.
- In the next 3 Shorts on the same topic, add "पूरा वीडियो: <long video URL>" to the YouTube description.

## 5. Quota and logging
- Long upload uses the uploads bucket (1 per upload); captions/thumbnail/playlist/comment use units — stay within the existing ledger.
- Log each long video (topic, format, segments with source id+timestamps, duration, URL) in sources/long_log.md, committed.
- Commit sources/ and tools/ changes, push. Print one line: YT LONG ON, with the first two planned topics and their post dates.
