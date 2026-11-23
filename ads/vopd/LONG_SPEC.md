# JSLL Virtual OPD long-form ad (5+ min) — PROTOTYPE 1
Requested by Sahil Jain (COO, JSLL), 23 Nov 2026 22:32 IST. Paid-ad creative for Jeena Sikho HiiMS Virtual OPD.
Do NOT post, do NOT add to queue.json. Render one prototype in two formats for internal + legal review first; scale to more only after approval.
Run after the 15 short ads job finishes (or with nice in parallel); never block the 01:00 nightly pipeline.

## Concept
Acharya Manish Ji, in one of his official webinars/lives, talks to patients about a patient's journey -> real patient experience clips from the official channel -> a calm voice-over endplate explaining how Virtual OPD works.
Total 5:00-6:30 min. Two renders of the same edit:
- landscape 1920x1080 (native webinar framing, no crop)
- vertical 1080x1920 (face/speaker-crop + framing QC, same as channel)

## Structure (target timings)
1. 0:00-0:12 Hook: strongest single line of Acharya Ji from the chosen webinar segment (lifestyle/approach, not a cure line). Big hook text overlay.
2. 0:12-2:45 Acharya Ji explaining a patient's story to the audience: what the patient changed (food, daily routine, sleep, discipline, consulting a doctor regularly), how the doctor guided them. Use ONE continuous or 2-3 stitched webinar windows (caption-first selection from YouTube captions, like WEBINAR_MODE).
3. 2:45-4:45 Patient experience: 2-3 short clips from official testimonial videos on the channel (search the channel for "Patient Experience", "Patient Feedback", "True Patient Feedback" titles). Keep only lines about the EXPERIENCE: being heard by the doctor, the diet and routine guidance, the convenience, how they feel about the care. Lower-third: "मरीज़ का अनुभव · हर व्यक्ति का अनुभव अलग हो सकता है".
4. 4:45-5:20 Acharya Ji line that encourages consulting a doctor and following guidance (and, if available, "doctor से पूछे बिना कोई दवा बंद न करें").
5. Endplate 25-35 s (voice-over, see script), branded card over blurred last frame.
Persistent small footer from 0:12 to the end: "Individual experiences vary · This is not a claim of cure · Consult your doctor".

## Hard compliance rules (Drugs & Magic Remedies Act, ASCI healthcare + testimonial guidelines, Meta health ads, DPDP)
- REMOVE every line, word or on-screen text that states or implies treatment/cure/reversal/"theek ho gaya"/"dawai band ho gayi"/report numbers (sugar, creatinine, HbA1c, BP readings)/dialysis stopped/surgery avoided/"guarantee"/time-bound results, for ANY disease. If a testimonial clip can't be cut without these, drop the clip.
- Do NOT name scheduled diseases in hooks, overlays, titles or the voice-over (diabetes, BP, cancer, kidney, liver, heart, thyroid, obesity, infertility, etc.). If Acharya Ji says a disease word in passing inside an otherwise compliant sentence, cut that sentence.
- No before/after, no lab reports or prescriptions on screen, no phone numbers, no hospital/camp promotion audio from the source, no Dr. Biswaroop footage or voice.
- Patient faces/names: only from testimonial videos already published on the official channel. List each patient clip (video id + timestamps) in index so Legal can confirm signed consent covers paid-ad use.

## Voice-over endplate (Google Cloud TTS hi-IN Chirp 3 HD; render two versions: female and male; generic voice, never clone a real person)
"आयुर्वेद में इलाज सिर्फ़ दवा नहीं, सही खान-पान, दिनचर्या और सही सलाह का साथ है।
अब Jeena Sikho HiiMS की वर्चुअल ओपीडी में आप घर बैठे हमारे आयुर्वेद डॉक्टरों से वीडियो कॉल पर बात कर सकते हैं।
अपनी समस्या बताइए, डॉक्टर आपकी दिनचर्या और खान-पान को समझेंगे और आपको सही मार्गदर्शन देंगे।
नीचे दिए लिंक पर क्लिक करें और आज ही अपनी वीडियो कंसल्टेशन बुक करें।"
(For TTS only, write "HiiMS" as "हिम्स" if mispronounced.)
On-screen endplate: Jeena Sikho HiiMS · Virtual OPD / घर बैठे आयुर्वेद डॉक्टर से वीडियो पर सलाह / 👉 नीचे दिए लिंक पर अभी बुक करें / footer: AI voice · Individual experiences vary · Not a claim of cure.

## Audio/visual
- Burned-in Hindi captions (Chirp transcription, caption cleanup) in both formats; landscape captions bottom-centre.
- loudnorm -14 LUFS; duck source under voice-over; light music bed only under the endplate (royalty-free, or none).
- Clean cuts between segments (0.3 s crossfade), no jump cuts mid-word.

## Output
- ads/vopd/long/vopd_long_01_landscape_F.mp4, _landscape_M.mp4, _vertical_F.mp4, _vertical_M.mp4 (same edit, two voices). If files exceed GitHub's 100 MB limit, encode at a lower bitrate (crf 26-28, 720p for landscape review copy) and keep the full-quality masters on the VM in /opt/aks/ads/long/.
- ads/vopd/long/index.md: segment-by-segment edit list (source video id, start-end, what is said in 1 line), every line removed for compliance and why, patient clip list for consent check, total duration.
- Print "VOPD LONG READY".
