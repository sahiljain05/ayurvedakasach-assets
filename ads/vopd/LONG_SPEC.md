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
(No disclaimer footer on any VOPD output: removed per user decision 23 Nov, FULL_AD.md part 0.)

## Hard compliance rules (Drugs & Magic Remedies Act, ASCI healthcare + testimonial guidelines, Meta health ads, DPDP)
- REMOVE every line, word or on-screen text that states or implies treatment/cure/reversal/"theek ho gaya"/"dawai band ho gayi"/report numbers (sugar, creatinine, HbA1c, BP readings)/dialysis stopped/surgery avoided/"guarantee"/time-bound results, for ANY disease. If a testimonial clip can't be cut without these, drop the clip.
- Do NOT name scheduled diseases in hooks, overlays, titles or the voice-over (diabetes, BP, cancer, kidney, liver, heart, thyroid, obesity, infertility, etc.). If Acharya Ji says a disease word in passing inside an otherwise compliant sentence, cut that sentence.
- No before/after, no lab reports or prescriptions on screen, no phone numbers, no hospital/camp promotion audio from the source, no Dr. Biswaroop footage or voice.
- Patient faces/names: only from testimonial videos already published on the official channel. List each patient clip (video id + timestamps) in index so Legal can confirm signed consent covers paid-ad use.

## Voice-over endplate (changed 23 Nov per ENDPLATE_VO.md part 3)
The closing voice-over is L1 for the female version and L2 for the male version; reuse the WAVs from ENDPLATE_VO.md part 1 as is
(Google Cloud TTS hi-IN Chirp 3 HD, generic synthetic voice, never a clone of a real person):
- Female: ads/vopd/vo/L1_F.wav (hi-IN-Chirp3-HD-Pulcherrima)
- Male: ads/vopd/vo/L2_M.wav (hi-IN-Chirp3-HD-Alnilam; 19.3 s, accepted as is by the user)
L1 (natural healing): क्या आप अपनी सेहत के लिए आयुर्वेद और प्राकृतिक तरीकों को अपनाना चाहते हैं? अब जीना सीखो हिम्स की वर्चुअल ओपीडी में, घर बैठे, वीडियो कॉल पर हमारे आयुर्वेद डॉक्टरों से बात कीजिए। डॉक्टर आपकी बात ध्यान से सुनेंगे, आपकी दिनचर्या और खान-पान समझेंगे, और आयुर्वेद के नज़रिए से आपको मार्गदर्शन देंगे। नीचे दिए लिंक पर क्लिक करें और अपनी वीडियो कंसल्टेशन बुक करें।
L2 (second opinion): अपनी सेहत को लेकर एक दूसरी राय चाहते हैं? जीना सीखो हिम्स की वर्चुअल ओपीडी में, आयुर्वेद डॉक्टर से घर बैठे वीडियो पर विस्तार से बात कीजिए। अपनी रिपोर्ट्स और अब तक का अनुभव साथ रखिए; डॉक्टर आपकी पूरी बात समझकर आयुर्वेद के अनुसार सलाह देंगे। नीचे दिए लिंक से आज ही अपनी वीडियो कंसल्टेशन बुक करें।
(The old 4-sentence voice-over script is replaced.) The endplate length follows the VO (VO is never cut or sped up).
On-screen endplate: Jeena Sikho HiiMS · Virtual OPD / घर बैठे आयुर्वेद डॉक्टर से वीडियो पर सलाह / Natural healing · Second opinion / 👉 नीचे दिए लिंक पर अभी बुक करें (no footer: removed per user decision 23 Nov, FULL_AD.md part 0).
No "cure", "theek kar denge", "jad se khatm", disease names, or stop-medicine hints anywhere in endplates.

## Audio/visual
- Burned-in Hindi captions (Chirp transcription, caption cleanup) in both formats; landscape captions bottom-centre.
- loudnorm -14 LUFS; duck source under voice-over; light music bed only under the endplate (royalty-free, or none).
- Clean cuts between segments (0.3 s crossfade), no jump cuts mid-word.

## Output
- ads/vopd/long/vopd_long_01_landscape_F.mp4, _landscape_M.mp4, _vertical_F.mp4, _vertical_M.mp4 (same edit, two voices). If files exceed GitHub's 100 MB limit, encode at a lower bitrate (crf 26-28, 720p for landscape review copy) and keep the full-quality masters on the VM in /opt/aks/ads/long/.
- ads/vopd/long/index.md: segment-by-segment edit list (source video id, start-end, what is said in 1 line), every line removed for compliance and why, patient clip list for consent check, total duration.
- Print "VOPD LONG READY".
