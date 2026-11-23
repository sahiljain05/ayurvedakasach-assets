# YouTube SEO for Ayurveda Ka Sach Shorts (user approved, 24 Nov)

Apply to every new YouTube upload (tools/post_yt.py) AND update the 6 already-uploaded videos with videos.update (aks001 QYcWlTrNwhM, LmpEEPMpNLI_c1 WoC8Xr3cvSI, NrQgIBqJlWs_c1 hi06U8_xo30, w5EpsKIMGIA_c1 V6aIo19JxZ4, w5EpsKIMGIA_c2 iBdXOBozl40, w5EpsKIMGIA_c3 dXtD4qgLJVE). Instagram/Facebook captions stay as they are; this is YouTube-only metadata.

## 1. Keyword per clip
- From the clip's transcript, pick ONE primary search phrase people in India actually type (Hindi or Hinglish as people type it, e.g. "दूध के साथ फल", "khali pet pani peene ke fayde", "raat ko dahi khana chahiye ya nahi"), plus 3-5 secondary phrases.
- Validate with YouTube autocomplete (free, no quota): GET https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=hi&gl=IN&q=<phrase>. Prefer a phrase (or its closest variant) that appears in suggestions. Cache results in work/yt_kw_cache.json. If the endpoint is unreachable, fall back to the transcript phrase.
- Never use disease names, "cure", "ilaj", "jad se khatm", "guaranteed", "100%", or any claim the clip does not make. Run the existing caption_problems() check on title, description and tags.

## 2. Title (YouTube only)
- 40-70 characters, primary phrase in the first 3-4 words, curiosity but not clickbait, must match what Acharya Ji actually says.
- Pattern examples: "दूध के साथ फल खाना सही या गलत? | Acharya Manish Ji", "खाली पेट पानी कब पिएं? आयुर्वेद का नियम".
- Hindi in Devanagari; one English/Hinglish keyword allowed when that is how people search. No ALL CAPS, max 1 emoji, no #Shorts in the title (YouTube detects Shorts by format).

## 3. Description
- Line 1-2 (shown in search): primary phrase + one-sentence summary of what the viewer learns, in natural Hindi.
- Then 3-5 short lines of the key points from the clip (no new claims).
- Then: "🎥 Acharya Manish Ji (official channel): <source video URL>" — linking the full source video.
- Then the 📚 संदर्भ block only if the clip already has one (CAPTION_FIX.md rules).
- Then the ⚠️ disclaimer line already used on the channel captions.
- Last line: exactly 3 hashtags (YouTube shows the first 3 above the title): #आयुर्वेद plus 2 topic hashtags (e.g. #AyurvedaTips #Diet). Plus #Shorts at the end (total ≤ 5 hashtags).
- 600-1,500 characters total.

## 4. Tags and fields
- tags: primary phrase, its Hinglish/English variant, 3-5 secondary phrases, "Acharya Manish Ji", "आचार्य मनीष जी", "Ayurveda Ka Sach", "आयुर्वेद". Max 15 tags, ≤ 450 characters total.
- categoryId 27 (Education), defaultLanguage "hi", defaultAudioLanguage "hi", privacyStatus "public", selfDeclaredMadeForKids false, notifySubscribers true for daily uploads, false for the 6 metadata updates.
- localizations: add an "en" title + 1-line description (English translation) so English searches also match.

## 5. Captions (helps search indexing)
- Upload the clip's Hindi transcript as an SRT caption track (captions.insert, language "hi", name "Hindi", 400 units) — we already have timed Hindi text from Chirp for every clip. Do this for new uploads and the 6 existing videos.

## 6. Playlists
- Create (once) and maintain topic playlists with SEO titles + descriptions: "आहार और खान-पान | Ayurveda Diet", "दिनचर्या | Daily Routine", "पाचन और पेट | Digestion Tips", "पानी और पेय | Water & Drinks", "आयुर्वेद की बातें | Acharya Manish Ji". Add each video to the 1 best-fit playlist (playlistItems.insert, 50 units).

## 7. Pinned comment
- After upload, post one comment from the channel asking a simple question related to the clip (e.g. "आप दूध के साथ कौन सा फल खाते हैं? 👇") and pin it if the API allows; if pinning is not available, just post it. No links in the comment.

## 8. Quota and safety
- Units per video: update/thumbnail/playlist 50 each, captions.insert 400, comment 50. Stay inside the existing ledger (≤ 8,000 units/day, ≤ 90 uploads/day). Spread the 6 backfill updates if needed.
- Do not change posting times, IG/FB posting, QC or the clip selection.
- Log each video's final title, description, tags, playlist and caption status to logs/yt_seo.log and queue.json (yt_title, yt_tags).
- Commit tools/ and sources/ changes, push. Print one line: YT SEO ON, with the 6 updated titles.
