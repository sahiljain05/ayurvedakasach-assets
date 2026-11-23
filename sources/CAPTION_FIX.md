# Caption fix (user request, 23 Nov 2026 21:36 IST)

Seen on the posted reel "पहले नहाएं या पहले नाश्ता? आयुर्वेद का नियम":

## Problem 1: research appears twice
The caption already has a "📚 Research:" block, and post_ig.py (build_caption) appends a second "📚 Research / संदर्भ:" block containing the long English `what_it_shows` notes. The disclaimer ends up in the middle.

Fix:
- Exactly ONE research section per caption, placed after the explanation and before the disclaimer.
- Hindi/Hinglish, short: one line per reference = reference name + max ~12 words of what it says. Never paste the English `what_it_shows` text into captions (keep it in queue.json only, for our records).
- build_caption must not append a research block if the caption already contains one (or, simpler: build the research block only in build_caption and strip it from the generated caption text).
- Order: title → explanation (2-3 lines) → 📚 संदर्भ (optional) → 🎥 Clip credit → ⚠️ disclaimer → hashtags.

## Problem 2: no negative / self-undermining lines
Never write lines like "कोई modern trial नहीं मिला", "no modern trial on bath timing", "evidence weak", "classical guidance only" in captions.
- If there is no modern study: list only the classical reference (e.g. "• अष्टांग हृदय, सूत्रस्थान 2.18: भोजन के तुरंत बाद स्नान उचित नहीं बताया गया"), or skip the research section entirely.
- Still never invent a citation, and never imply science proves something that only a classical text says.

## Apply to
post_ig.py, post_fb.py, post_one.py, app/daily_prompt.md, app/select_prompt.md (backups first).

## Then
1. Rewrite captions of all clips with status `ready` in queue.json to the new format; push.
2. Already-posted Facebook reels: edit the description via Graph API if supported (POST /{video_id} with description). Report which ones changed.
3. Already-posted Instagram reels: the API cannot edit IG captions. List their permalinks plus the corrected caption text for each in sources/ig_caption_corrections.md so the user can paste them manually in the Instagram app.
4. Print "CAPTION FIX DONE".
