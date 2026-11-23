# JSLL Virtual OPD ad reels (separate from Ayurveda Ka Sach channel)
Requested by Sahil Jain (COO, JSLL), 23 Nov 2026. These are paid-ad creatives for Jeena Sikho HiiMS Virtual OPD lead generation.
Do NOT add these to queue.json, do NOT post them anywhere, do NOT touch .autopost. Render and push for review only.

## Deliverable
15 reels, 9:16, 1080x1920, 20-35 s each:
- Body: 15-28 s clip of Acharya Manish Ji from his official long-form YouTube videos (reuse already-downloaded sources and the regular pipeline steps: Chirp transcription, caption cleanup, face/speaker-crop, framing QC). One clear everyday lifestyle tip per reel with a strong 1-line hook overlay in the first 3 s. Burned-in Hindi captions like the channel reels.
- Endplate: last 5 s. Clean branded card (no Acharya Ji footage behind it needed; a blurred last frame is fine):
  Line 1 (large): Jeena Sikho HiiMS
  Line 2: Virtual OPD · घर बैठे डॉक्टर से वीडियो पर सलाह
  Line 3: 👉 नीचे दिए लिंक पर अभी बुक करें
  Footer (small): AI voice · Educational content, not a cure claim
  (No price, no phone number, no URL burned in: the ad's CTA button carries the landing-page link.)
- Endplate voice-over: Google Cloud Text-to-Speech, language hi-IN, Chirp 3 HD voices (list available hi-IN Chirp3-HD voices first and pick ONE natural male and ONE natural female). Use the VM metadata token (cloud-platform scope; API already enabled). This is a generic synthetic voice: never clone or imitate Acharya Ji or any real person.
  Duck the clip audio under the voice-over; voice-over must fit within the 5 s endplate (speakingRate up to 1.1 if needed).
- Split: 8 reels female voice, 7 male voice. Rotate the 4 scripts below evenly.

## Endplate scripts (Hindi, use exactly)
S1: अब घर बैठे आयुर्वेद डॉक्टर से वीडियो पर सलाह लें। Jeena Sikho HiiMS वर्चुअल ओपीडी — नीचे दिए लिंक पर अभी बुक करें।
S2: सेहत से जुड़े सवाल हैं? Jeena Sikho HiiMS के डॉक्टरों से वीडियो कंसल्टेशन लें — नीचे लिंक पर क्लिक करें।
S3: डॉक्टर के पास जाने की भागदौड़ नहीं। Jeena Sikho HiiMS वर्चुअल ओपीडी में वीडियो पर बात करें — अभी बुक करें।
S4: सही खान-पान और दिनचर्या की सलाह, अब वीडियो कॉल पर। Jeena Sikho HiiMS — नीचे लिंक से अपॉइंटमेंट लें।
Pronunciation: if TTS mispronounces "HiiMS", use "हिम्स" in the SSML/text sent to TTS only (keep "HiiMS" in on-screen text).

## Ad compliance (stricter than the channel)
- Drugs & Magic Remedies Act, ASCI healthcare guidelines, Meta health ad policy.
- Body clip must NOT mention any disease treatment, cure, reversal, guarantee, stopping medicine, or scheduled diseases (diabetes, BP, cancer, kidney, liver, heart, thyroid, obesity, infertility, etc.) even in passing. Pick pure lifestyle tips only: food combinations, eating habits, daily routine, sleep, water, breathing, seasonal habits.
- No "Do you have X?" personal-health hooks, no before/after, no testimonials, no numbers promising results.
- No Dr. Biswaroop footage or voice.

## Output
- Files: ads/vopd/vopd_ad_01.mp4 ... vopd_ad_15.mp4, plus ads/vopd/contact_sheet_XX.jpg per reel.
- ads/vopd/index.md: table with file, source video id + timestamps, hook, endplate script (S1-S4), voice (name, M/F), duration, compliance notes.
- Delete large intermediate files after rendering. Push to git. Print "VOPD ADS READY".
