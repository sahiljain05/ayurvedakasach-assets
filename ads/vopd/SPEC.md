# JSLL Virtual OPD ad reels (separate from Ayurveda Ka Sach channel)
Requested by Sahil Jain (COO, JSLL), 23 Nov 2026. These are paid-ad creatives for Jeena Sikho HiiMS Virtual OPD lead generation.
Do NOT add these to queue.json, do NOT post them anywhere, do NOT touch .autopost. Render and push for review only.

## Deliverable
15 reels, 9:16, 1080x1920, 20-35 s each:
- Body: 15-28 s clip of Acharya Manish Ji from his official long-form YouTube videos (reuse already-downloaded sources and the regular pipeline steps: Chirp transcription, caption cleanup, face/speaker-crop, framing QC). One clear everyday lifestyle tip per reel with a strong 1-line hook overlay in the first 3 s. Burned-in Hindi captions like the channel reels.
- Endplate: last 5-7 s (endplate may run up to 7 s so S1/S2 fit at rate ≤ 1.1). Clean branded card (no Acharya Ji footage behind it needed; a blurred last frame is fine):
  Jeena Sikho HiiMS · Virtual OPD / घर बैठे आयुर्वेद डॉक्टर से वीडियो पर सलाह / Natural healing · Second opinion / 👉 नीचे दिए लिंक पर अभी बुक करें
  (No disclaimer footer on any VOPD output: removed per user decision 23 Nov, FULL_AD.md part 0.)
  (No price, no phone number, no URL burned in: the ad's CTA button carries the landing-page link.)
- Endplate voice-over: Google Cloud Text-to-Speech, language hi-IN, Chirp 3 HD voices (list available hi-IN Chirp3-HD voices first and pick ONE natural male and ONE natural female). Use the VM metadata token (cloud-platform scope; API already enabled). This is a generic synthetic voice: never clone or imitate Acharya Ji or any real person.
  Duck the clip audio under the voice-over; voice-over must fit within the endplate (speakingRate ≤ 1.1; endplate may run up to 7 s so S1/S2 fit at rate ≤ 1.1).
- Split: 8 reels female voice, 7 male voice. Alternate the 2 scripts below (S1, S2, S1, ...).

## Endplate scripts (Hindi, use exactly)
Changed 23 Nov per ENDPLATE_VO.md part 3: the old S1-S4 are replaced by only these two (alternate them; keep the 8 F / 7 M split).
S1: आयुर्वेद और प्राकृतिक तरीकों पर सलाह चाहिए? घर बैठे जीना सीखो हिम्स के डॉक्टर से वीडियो पर बात करें — नीचे लिंक पर बुक करें।
S2: अपनी सेहत पर दूसरी राय चाहिए? जीना सीखो हिम्स वर्चुअल ओपीडी — घर बैठे वीडियो कंसल्टेशन, नीचे दिए लिंक से बुक करें।
Endplate may run up to 7 s so S1/S2 fit at rate ≤ 1.1.
No "cure", "theek kar denge", "jad se khatm", disease names, or stop-medicine hints anywhere in endplates.

## Ad compliance (stricter than the channel)
- Drugs & Magic Remedies Act, ASCI healthcare guidelines, Meta health ad policy.
- Body clip must NOT mention any disease treatment, cure, reversal, guarantee, stopping medicine, or scheduled diseases (diabetes, BP, cancer, kidney, liver, heart, thyroid, obesity, infertility, etc.) even in passing. Pick pure lifestyle tips only: food combinations, eating habits, daily routine, sleep, water, breathing, seasonal habits.
- No "Do you have X?" personal-health hooks, no before/after, no testimonials, no numbers promising results.
- No Dr. Biswaroop footage or voice.

## Output
- Files: ads/vopd/vopd_ad_01.mp4 ... vopd_ad_15.mp4, plus ads/vopd/contact_sheet_XX.jpg per reel.
- ads/vopd/index.md: table with file, source video id + timestamps, hook, endplate script (S1/S2), voice (name, M/F), duration, compliance notes.
- Delete large intermediate files after rendering. Push to git. Print "VOPD ADS READY".
