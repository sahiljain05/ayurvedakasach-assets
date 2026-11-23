# VOPD endplate voiceovers + b-roll videos (user approved, 23 Nov)

Brand: Jeena Sikho HiiMS · Virtual OPD. Generic synthetic Hindi voice (Google Cloud TTS, hi-IN Chirp 3 HD). Never clone or imitate Acharya Ji or any real person.

## 1. Voiceovers (do now)

Use the VM metadata token (cloud-platform scope). List hi-IN Chirp3-HD voices; use the SAME female and male voice already picked for SPEC.md (if none picked yet, choose one natural female and one natural male and note them).
speakingRate 1.0 (allowed 0.95-1.08). Each VO must be 20-32 s. Encode LINEAR16 48 kHz, then save as WAV.

Make 4 files in ads/vopd/vo/: L1_F.wav, L1_M.wav, L2_F.wav, L2_M.wav

L1 (natural healing):
क्या आप अपनी सेहत के लिए आयुर्वेद और प्राकृतिक तरीकों को अपनाना चाहते हैं? अब जीना सीखो हिम्स की वर्चुअल ओपीडी में, घर बैठे, वीडियो कॉल पर हमारे आयुर्वेद डॉक्टरों से बात कीजिए। डॉक्टर आपकी बात ध्यान से सुनेंगे, आपकी दिनचर्या और खान-पान समझेंगे, और आयुर्वेद के नज़रिए से आपको मार्गदर्शन देंगे। नीचे दिए लिंक पर क्लिक करें और अपनी वीडियो कंसल्टेशन बुक करें।

L2 (second opinion):
अपनी सेहत को लेकर एक दूसरी राय चाहते हैं? जीना सीखो हिम्स की वर्चुअल ओपीडी में, आयुर्वेद डॉक्टर से घर बैठे वीडियो पर विस्तार से बात कीजिए। अपनी रिपोर्ट्स और अब तक का अनुभव साथ रखिए; डॉक्टर आपकी पूरी बात समझकर आयुर्वेद के अनुसार सलाह देंगे। नीचे दिए लिंक से आज ही अपनी वीडियो कंसल्टेशन बुक करें।

Use the text exactly. Add SSML breaks only at sentence ends (300 ms). Listen-check is not possible, so verify with ffprobe duration and Chirp transcription back (hi-IN) that every word is present; fix and regenerate if a word is missing.

Also write ads/vopd/vo/index.md: file, voice name, duration, speakingRate.

## 2. Videos (do when ads/vopd/broll/broll_16x9.mp4 exists after git pull; if not there yet, finish part 1, commit, push, and stop)

Write tools/vopd_broll_mux.py and run it for all 4 VOs. Input b-roll is a 26 s 1920x1080 silent MP4 whose last 4 s are the title card.
- VO starts at 0.4 s.
- If VO end (0.4 + dur) + 0.8 s > b-roll length: extend the video by holding the last frame (tpad stop_mode=clone) to VO end + 0.8 s. Never speed up or cut the VO.
- Else: pad audio with silence to the b-roll length.
- Audio: loudnorm to -16 LUFS, AAC 192k 48 kHz, mono is fine.
- Footer burned in for the whole video (libass, shaping=complex, font Noto Sans): bottom centre, 26 px, cream #F6EEDC text on a 55% dark bar, 24 px from the bottom edge:
  Consultation and guidance only · Do not stop or change ongoing treatment without your doctor's advice · Individual experiences vary · AI voice
- No price, no phone number, no URL on screen.
- H.264 crf 20 preset veryfast, yuv420p, +faststart.
Outputs: ads/vopd/endplate/vopd_endplate_L1_F.mp4, _L1_M, _L2_F, _L2_M, plus a contact sheet (6 frames each) ads/vopd/endplate/sheet_<name>.jpg.

## 3. Update the ad jobs' endplate scripts

Final approved endplate scripts replace the old ones:
- SPEC.md short reels: replace S1-S4 with only these two (alternate them; keep the F/M split):
  S1: आयुर्वेद और प्राकृतिक तरीकों पर सलाह चाहिए? घर बैठे जीना सीखो हिम्स के डॉक्टर से वीडियो पर बात करें — नीचे लिंक पर बुक करें।
  S2: अपनी सेहत पर दूसरी राय चाहिए? जीना सीखो हिम्स वर्चुअल ओपीडी — घर बैठे वीडियो कंसल्टेशन, नीचे दिए लिंक से बुक करें।
  Endplate card text: Jeena Sikho HiiMS · Virtual OPD / घर बैठे आयुर्वेद डॉक्टर से वीडियो पर सलाह / Natural healing · Second opinion / 👉 नीचे दिए लिंक पर अभी बुक करें
  Footer: Consultation and guidance only · Do not stop or change ongoing treatment without your doctor's advice · Individual experiences vary · AI voice
  Endplate may run up to 7 s so S1/S2 fit at rate ≤ 1.1.
- LONG_SPEC.md: the closing voiceover is L1 (for F) and L2 (for M), reuse the WAVs from part 1; same footer.
- No "cure", "theek kar denge", "jad se khatm", disease names, or stop-medicine hints anywhere in endplates.
If a VOPD job is still running, let it finish, then re-render only the endplates of already-made outputs with the new scripts (body clips unchanged). Update ads/vopd/index.md.

## Finish
git add, commit, push. Print exactly one line at the end: ENDPLATE VO READY (and, if part 2 ran, ENDPLATE VIDEOS READY).
