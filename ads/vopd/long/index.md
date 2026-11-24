# JSLL Virtual OPD long-form ad · PROTOTYPE 1 (LONG_SPEC.md) · for internal + Legal review only

NOT posted, NOT queued (queue.json untouched). Built 23 Nov 2026 by the vopdlong job (scripts: /opt/aks/app/vopd/long/).
Same edit in 4 files: landscape 1920x1080 (native webinar framing; non-16:9 sources fit over a blurred fill) and vertical
1080x1920 (render.py face/speaker-crop + face QC, as on the channel), each with the female (L1) and male (L2) endplate.

## Files
| file | duration | parts | resolution / audio | integrated loudness | size (git copy) |
|---|---|---|---|---|---|
| vopd_long_01_landscape_F.mp4 | 5:05.4 (305.4 s) | body 279.9 s + endplate 25.8 s (VO 22.26 s, starts 4:39.63) | 1920x1080 (master 1920x1080), AAC 48000 Hz 2ch | -14.1 LUFS (TP -1.3 dBFS) | 94.1 MB (master 94 MB) |
| vopd_long_01_landscape_M.mp4 | 5:04.6 (304.6 s) | body 279.9 s + endplate 25.0 s (VO 19.31 s, starts 4:39.63) | 1920x1080 (master 1920x1080), AAC 48000 Hz 2ch | -14.1 LUFS (TP -1.6 dBFS) | 94.0 MB (master 94 MB) |
| vopd_long_01_vertical_F.mp4 | 5:05.5 (305.5 s) | body 280.1 s + endplate 25.8 s (VO 22.26 s, starts 4:39.77) | 720x1280 (master 1080x1920), AAC 48000 Hz 2ch | -14.3 LUFS (TP -2.6 dBFS) | 31.3 MB (master 111 MB) |
| vopd_long_01_vertical_M.mp4 | 5:04.8 (304.8 s) | body 280.1 s + endplate 25.0 s (VO 19.31 s, starts 4:39.77) | 720x1280 (master 1080x1920), AAC 48000 Hz 2ch | -14.3 LUFS (TP -2.6 dBFS) | 31.2 MB (master 111 MB) |

Target 5:00–6:30: met (see durations). Full-quality masters (crf 20) stay on the VM in /opt/aks/ads/long/. The landscape files here ARE the
1920x1080 masters (94 MB, under the 95 MB limit). The vertical masters are 111 MB, so the vertical files here are 720x1280 crf 26
review copies.

## Edit list (same for all 4 files; times in the female version, male endplate is 0.76 s shorter)
Segment joins are 0.3 s crossfades (video + audio); every segment starts at a sentence start and ends on a complete sentence
(word timings, start = first word − 0.15 s). Captions: Chirp 3 transcription of the cut window only + caption cleanup against the
YouTube captions; burned in for every segment (landscape bottom-centre, vertical as render.py).

| seg | spec part | at | source (YouTube id, source timestamps) | length | speaker / type | what is said (1 line) | vertical face QC |
|---|---|---|---|---|---|---|---|
| s01 | 1 hook + 2 | 0:00.00 | [GPFnAqxDBWM](https://www.youtube.com/watch?v=GPFnAqxDBWM&t=1778s) 29:38.33–30:00.68 | 22.4 s | Acharya Ji · official live | आप सिर्फ तीन आदतें सुधार लो अपनी। ... वज्रासन में खाना ... डाइनिंग टेबल छोड़ दो ... लकड़ी की चौकी ... ऐसे बैठ के खाना खाना है। | PASS |
| s02 | 2 | 0:22.35 | [wzWy5cSjXls](https://www.youtube.com/watch?v=wzWy5cSjXls&t=4544s) 75:44.09–75:58.04 | 13.9 s | Acharya Ji · official live | कहना मानो, डाइट का ध्यान रखो। सूरज डूबने के बाद ... खाना बंद करो। हफ्ते में एक उपवास ... नाश्ते में फ्रूट्स पहले ... लंच में सैलेड पहले ... डिनर में वेजिटेबल सूप पहले पियो। | PASS |
| s03 | 2 | 0:36.30 | [Wd2ia1AycRY](https://www.youtube.com/watch?v=Wd2ia1AycRY&t=254s) 4:14.25–4:29.60 | 15.3 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | finish dinner about 4 hours before sleep; sleep by 10:30-11 (short-ads reel 10 window, already verified) | PASS |
| s04 | 2 | 0:51.65 | [DmWr7zGSa84](https://www.youtube.com/watch?v=DmWr7zGSa84&t=2798s) 46:38.61–46:54.08 | 15.5 s | Acharya Ji · official live | एक बटन दबाते हो सारी लाइटें जलाते हो, वो सबसे बड़ी गलती है। हर कमरे में एक जीरो वाट का बल्ब लगाओ ... अगर रात को नींद खुले तो वो लाइट चलानी है। | PASS |
| s05 | 2 | 1:07.12 | [Wd2ia1AycRY](https://www.youtube.com/watch?v=Wd2ia1AycRY&t=73s) 1:13.78–1:32.00 | 18.2 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | sleep with head east/south, lie on the left side, get up on the right side (short-ads reel 03 window) | PASS |
| s06 | 2 | 1:25.34 | [Wd2ia1AycRY](https://www.youtube.com/watch?v=Wd2ia1AycRY&t=97s) 1:37.05–1:54.60 | 17.6 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | morning squat (malasan) with warm water (short-ads reel 08 window) | PASS |
| s07 | 2 | 1:42.89 | [LmpEEPMpNLI](https://www.youtube.com/watch?v=LmpEEPMpNLI&t=429s) 7:09.85–7:28.30 | 18.4 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | chew food until it is liquid, sip water slowly (short-ads reel 06 window) | PASS |
| s08 | 2 | 2:01.34 | [LmpEEPMpNLI](https://www.youtube.com/watch?v=LmpEEPMpNLI&t=350s) 5:50.75–6:14.80 | 24.1 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | no water with meals, sips only, 30-40 min gap (short-ads reel 02 window) | PASS |
| s09 | 2 | 2:25.39 | [MSI6qazPVCw](https://www.youtube.com/watch?v=MSI6qazPVCw&t=95s) 1:35.85–1:55.50 | 19.6 s | Acharya Ji · official long-form video (NOT a live, see deviation 1) | hug and appreciate family; food carries emotion (short-ads reel 13 window) | PASS |
| s10 | 3 | 2:45.04 | [cUDCBTgLMdQ](https://www.youtube.com/watch?v=cUDCBTgLMdQ&t=11s) 0:11.93–0:25.60 | 13.7 s | Patient testimonial (official channel) | डॉक्टर से लेकर के और जो दूसरा एंप्लॉईस हैं ... इतने कोऑपरेटिव हैं कि यह पता ही नहीं लगने देते कि यह पेशेंट है या अटेंडेंट है। | PASS |
| s11 | 3 | 2:58.71 | [cUDCBTgLMdQ](https://www.youtube.com/watch?v=cUDCBTgLMdQ&t=46s) 0:46.37–0:58.00 | 11.6 s | Patient testimonial (official channel) | जो बच्चियां यहां पर जो काम करती हैं ... इतनी कोऑपरेटिव हैं कि पेशेंट को यह अपना फैमिली मेंबर ही समझते हैं। | PASS |
| s12 | 3 | 3:10.34 | [cUDCBTgLMdQ](https://www.youtube.com/watch?v=cUDCBTgLMdQ&t=62s) 1:02.89–1:09.84 | 7.0 s | Patient testimonial (official channel) | यह अपना फैमिली मेंबर समझते हैं और वह साक्षी, डॉक्टर साक्षी जी हैं। वह तो ऐसे लगता है जैसे कि वह मेरी बेटी होनी चाहिए थी। | PASS |
| s13 | 3 | 3:17.29 | [nY-dOIsS4NU](https://www.youtube.com/watch?v=nY-dOIsS4NU&t=16s) 0:16.41–0:42.72 | 26.3 s | Patient testimonial (official channel) | मैडम जो हम आपको यहां पे डाइट देते हैं वो आपको कैसी लगी? ... डाइट तो बहुत अच्छी है ... हर चीज टाइमली मिलती है ... फ्रेश ... यहां पे डिसिप्लिन है टाइम में भी ... बहुत अच्छा तालमेल। | PASS |
| s14 | 3 | 3:43.60 | [nY-dOIsS4NU](https://www.youtube.com/watch?v=nY-dOIsS4NU&t=69s) 1:09.85–1:40.88 | 31.0 s | Patient testimonial (official channel) | मैडम आप ये बताइए ... स्टाफ का बिहेवियर कैसा लगता है? स्टाफ भी बहुत अच्छा है। सबके अंदर बड़ा ही सेवा भाव ... क्लीननेस भी बहुत ज्यादा है ... पूरी सुविधा प्रोवाइड कर रहे हैं हमें। | PASS |
| s15 | 4 | 4:14.63 | [nU2PjgftoNk](https://www.youtube.com/watch?v=nU2PjgftoNk&t=5843s) 97:23.73–97:35.16 | 11.4 s | Acharya Ji · official live | एक चीज सुनो ध्यान से। मेरे से मिलने से भी कुछ नहीं होना। मैंने भी ड्यूटी डॉक्टर की लगानी है ... करने वाले तो डॉक्टर हैं। | PASS |
| s16 | 4 | 4:26.06 | [nU2PjgftoNk](https://www.youtube.com/watch?v=nU2PjgftoNk&t=5885s) 98:05.81–98:19.28 | 13.5 s | Acharya Ji · official live | 900 डॉक्टर्स की टीम है। सब मिलके लगे हुए हैं। लेकिन फॉलो आपको करना है। जो आपको डाइट बताई जाएगी, जो आपको सोने का उठने का टाइम बताया जाएगा। आप लोगों ने प्रकृति के करीब जाना है। | PASS |
| EP | 5 | body end | — | F 25.8 s / M 25.0 s | voice-over endplate | branded card over the blurred last frame; VO L1_F.wav (female) / L2_M.wav (male) reused as is; VO starts 1.0 s into the card, ≥2.5 s tail | — |

Hook overlay (0:00.2–0:11.5): "बस अपनी आदतें सुधार लो". Patient lower-third on s10–s14: "मरीज़ का अनुभव · हर व्यक्ति का अनुभव अलग हो सकता है". No disclaimer footer anywhere
(user decision 23 Nov, FULL_AD.md part 0). No music bed (spec allows "or none"); the endplate has no source audio, so nothing to duck.

## Patient clips for Legal's consent check (paid-ad use)
Both are published on the official Acharya Manish Ji channel. Faces and voices are shown; no names on screen (spoken names below).
| clip | video | timestamps used | person | spoken in clip | on-screen changes |
|---|---|---|---|---|---|
| s10, s11, s12 | [cUDCBTgLMdQ](https://www.youtube.com/watch?v=cUDCBTgLMdQ) "HiiMS Hospital Patient Experience · Emotional Support & Healing Journey" (Short) | 0:11.9–0:25.6, 0:46.4–0:57.9, 1:02.9–1:09.8 | male patient, about 63 (says his age at 0:09, not used) | names staff "डॉक्टर साक्षी जी" | top 608x700 crop removes the source's burned-in caption "63 साल कि उम्र हो गई ऐसा हॉस्पिटल नहीं देखा" |
| s13, s14 | [nY-dOIsS4NU](https://www.youtube.com/watch?v=nY-dOIsS4NU) "HiiMS Hospital Diet Review · Real Patient Insights" | 0:16.4–0:42.7, 1:09.9–1:40.9 | female patient "श्वेता, दिल्ली" (named at 0:01, not used) + HiiMS staff interviewer | interviewer asks about diet and staff | crop 1316x740 at (528,0) removes the source's promo L-banner (disease names, phone number 82704-82704, doctor photos incl. Dr. Biswaroop), HiiMS logo and city ticker |

## Lines removed for compliance (and why)
| source | removed | reason |
|---|---|---|
| cUDCBTgLMdQ 0:00–0:11 | "हम लोगों ने और भी दिल्ली के ... हॉस्पिटल देखे हैं। लेकिन जो ह्यूमैनिटी इस हॉस्पिटल में ... कहीं नजर नहीं आई।" | comparison with other hospitals (ASCI comparative claim); when in doubt, removed |
| cUDCBTgLMdQ 0:26–0:46 | "पेशेंट को इतनी बेहतरीन तरीके से ट्रीट करते हैं कि वह बगैर मेडिसन भी यह सोचता है कि मैं ठीक हो रहा हूं। ..." | implies getting well / without medicine |
| cUDCBTgLMdQ 1:13–1:26 | "डाइटिशियन ... डॉक्टर अंकित ... ट्रीटमेंट का सिस्टम ..." | sentence not cleanly separable, mentions treatment; removed |
| cUDCBTgLMdQ burned-in caption | "63 साल कि उम्र हो गई ऐसा हॉस्पिटल नहीं देखा" | hospital comparison; cropped out |
| nY-dOIsS4NU 0:43–1:09 | "मिलेट्स ... हेल्थ के लिए बहुत ही अच्छी ... ओवर वेट ... वेट लॉस में, हमारी बीमारियों में भी बहुत ज्यादा ही फायदा ..." | weight-loss / disease-benefit result claim |
| nY-dOIsS4NU 1:41–end | "एक बार हॉस्पिटल आकर ... हेल्थ चेकअप जरूर कराएं ...", branch city list, "हर किडनी पेशेंट लीवर फेल के पेशेंट और कैंसर के पेशेंट तक ..." | hospital promotion audio, disease names |
| nY-dOIsS4NU on-screen | L-banner "किडनी फेल / STAGE 4 कैंसर / बी.पी / हार्ट प्रॉब्लम / शुगर / लीवर फेल / CALL NOW 82704-82704", doctor photos (incl. Dr. Biswaroop Roy Chowdhury) | disease names, phone number, excluded speaker's photo; cropped out |
| GPFnAqxDBWM 29:33–29:38 | "...अगर खाया होता तेरे को ये कैंसर होता भी ना। मैं मजाक नहीं कर रहा हूं।" (right before the hook) | disease name / prevention claim; hook starts at "आप सिर्फ" |
| GPFnAqxDBWM 30:00– | habit no. 2 (urinating while squatting) | not ad-appropriate; cut after habit 1 |
| wzWy5cSjXls 1:15:58–1:16:03 | "अगर आप सब ये लोग करते हो तो आप सबको आराम आएगा।" | benefit promise |
| wzWy5cSjXls (Zoom) | second participant's tile (patient in a surgical cap, under "Dr Vikas Jaswal Shudhigram"), meeting title "Webinar for All Disease Patients" | patient face not from a testimonial video; disease wording; cropped to Acharya Ji's tile |
| DmWr7zGSa84 46:28–46:38, 46:55– | "तो हमारा लीवर डिस्टर्ब हो जाता है, किडनी डिस्टर्ब हो जाती है ..." / "...लीवर अपना काम शुरू कर देगा, किडनी ..." | organ/disease words around the night-light tip |
| nU2PjgftoNk 1:37:35–1:38:02 | "अभी वो डॉक्टर ईश हैं ... गणेश जी ... नाक की ब्लीडिंग किसने बंद करी? ... डॉक्टर ने करी।" | treatment result (between the two s15/s16 pieces) |
| nU2PjgftoNk 1:38:20– | "...पार्क ... जूते ..." continuation ending "चार गुना फायदा ज्यादा होगा" | benefit claim |
| nU2PjgftoNk 1:38:02–1:38:05 | "मैं अकेला कुछ नहीं कर सकता तो पूरी टीम है।" | not compliance: he faces away from the camera (no face for the vertical QC); s16 starts at the next sentence |

Windows read and rejected (not used at all):
- **The Ganesh ji story** (8CImGfdXc5s 1:48:51, 6gqkQqlSAFo ~36:00): a publicly known blood-cancer case with bleeding-stopped and haemoglobin claims.
- **FErKHyVxioQ 1:05:29** ("मैडम धूप पे बैठ रही है, नंगे पांव घास पे…"): the screen showed a "Before / After" panel captioned "Liver ठीक होना…".
- **FErKHyVxioQ ~1:06:26:** "मैं ठीक हो सकता हूं".
- **DmWr7zGSa84 23:04** ("डाइट ठीक करी, सोने का उठने का टाइम ठीक करा"): inside a knee-repaired / surgery-avoided story.
- **iKl3n7UMlRg 36:36** (the pledge): a screen share with a wound/foot image, and Acharya Ji not on screen.
- **nU2PjgftoNk 15:20** ("eat only when really hungry"): the speaker is a guest, not Acharya Ji.
- **oAUTKUqdZzU 1:29:16:** the speaker is a guest doctor.
- **The kQ8NqDHca-s child story:** a time-bound promise in a cancer case.
- **oAUTKUqdZzU 59:00:** a 21 kg weight-loss claim.
- **wzWy5cSjXls 6:20–15:00:** a guest doctor speaking, with recovery claims.
- **Testimonial videos tcmtSwunGKI, HZIiB5L1SOQ, Efrvi2sr8gA, -CplblXHm-I, nwSFrO1B6Xo, 1C-SFmuLfd4, TxckjOaXKhQ, OfxOMxYV3ro, eC0krSOhK7M:** every line is a disease/cure/percent-improvement claim, plus a phone-number promo.
- **7WJuVwc8J4o:** garbled audio and the same promo banner.

## Deviations from LONG_SPEC.md (could not be done exactly as written)
1. **Segment 2: no compliant "patient's story" told by Acharya Ji exists in the official lives.** I screened the captions of 25 official
   lives/webinars, including a full read-through by a second pass. Every passage where Acharya Ji tells a patient's journey (food, routine,
   doctor guidance) sits inside a disease / cure / report-number / surgery-avoided story. Compliant pieces were only 6–30 s and about
   different patients, and the two usable-sounding ones failed on screen (Before/After panel) or context (knee story). So s01–s09 are
   **Acharya Ji's own lifestyle guidance** (what a person changes: how and when to eat, sun-down dinner, weekly fast, fruit/salad/soup first,
   sleep timing and position, night lights, morning routine, chewing, water with meals, family atmosphere). That is the spec's list of
   changes, but not told as one patient's story. 3 windows are from official lives (s01, s02, s04). To reach the 5:00 minimum, **6 windows
   (s03, s05–s09) come from Acharya Ji's official long-form videos, not lives**. They are the same windows the short-ads job already
   verified for SPEC.md reels 10, 03, 08, 06, 02, 13 (captions corrected and checked against YouTube captions). Remove them if only lives
   are acceptable; the ad would then be about 3:45.
   Because of this, segment 2 is a stitch of **9 short windows (13–24 s each)** instead of the spec's "ONE continuous or 2-3 stitched
   webinar windows". Segment 3 uses 5 pieces from 2 testimonial videos.
2. **The "doctor से पूछे बिना कोई दवा बंद न करें" line does not exist.** No line where Acharya Ji says not to stop medicine without asking
   the doctor was found in any screened live; his medicine statements point the other way and fail compliance. Segment 4 (s15–s16) is his
   "करने वाले तो डॉक्टर हैं … फॉलो आपको करना है, जो डाइट बताई जाएगी, सोने-उठने का टाइम …" (consult and follow the doctor's guidance).
   There is no stop-medicine hint anywhere in the ad. Not added as text or VO, because the spec asks for it only "if available" and
   FULL_AD.md removed the disclaimer footer.
3. **Timings differ from the targets.** Hook + segment 2: about 0:00–2:45 as targeted. Segment 3 (patients) is about 1:30 instead of 2:00,
   because only 2 testimonial videos had enough experience-only lines (about 90 s after cuts). Segment 4 is about 25 s instead of 35 s.
   Endplate F 25.8 s / M 25.0 s (VO-led, within 25–35 s). Totals are in the table above.
4. **Patient clips are in-hospital (IPD) experiences, not Virtual OPD experiences.** No Virtual-OPD testimonial was found on the channel.
   The lines used are about care, staff and diet routine only.
5. **Caption-first screening of the 25 lives used public YouTube auto-captions fetched with yt-dlp.** vidIQ had 22 credits, enough for only
   4 transcripts. vidiq_video_transcript was used to confirm the 2 patient videos (both match the windows and removed lines above).
   Only the chosen windows (±10 s) were downloaded (YouTube section download) and transcribed with Chirp 3; no full webinar was downloaded
   or sent to Chirp.
6. **Visible source text kept:**
   - s01 landscape shows a whiteboard in the background ("Food as medicine, Water as medicine …"); the vertical crop excludes it.
   - s02 is a Zoom recording upscaled from a 944x531 tile, so it looks slightly soft.
   - s10–s12 come from a 608 px-wide phone video, so they look soft at 1080 px.
   - s09/s08 (long-form) include the channel's own short b-roll/logo shots, as in the reels.
7. **Background people:** s15/s16 have seated audience members in a hospital hall, small and in the background of the landscape frame
   (not featured); the vertical crop is on Acharya Ji. Legal may want to check this.
8. **Voice-over:** L1_F.wav and L2_M.wav were reused unchanged (L2_M is 19.31 s, below ENDPLATE_VO.md's 20 s minimum, accepted by the
   user). No listen-check was possible; levels were checked with ebur128.

## Framing notes (vertical)
render.py framed s01–s12 (face/speaker-crop + face QC, all PASS). For 4 segments its automatic speaker-crop picked the wrong
subject, so I set the vertical crop by hand. render.py was not modified. Face positions were measured with the same face detector,
and the face QC (qc.py check()) was re-run on each result (all PASS):
- s13, s14 (patient interview): render.py showed the patient while the staff interviewer asked his question, and jumped to the frame
  edge or the interviewer while she answered. Manual time-based crop: interviewer during his question, patient during her answer.
- s15 (Acharya Ji): after the source's shot change (1:37:28) render.py's single crop showed the empty stage and a
  poster portrait for ~3 s while he walked; manual crop follows him.
- s16 (Acharya Ji): render.py's crop jumped 3 times to a large portrait poster behind the stage. Fixed crop on Acharya Ji, and the
  segment starts one sentence later (he faces away from the camera during "मैं अकेला कुछ नहीं कर सकता…").
Landscape keeps the native framing for every segment.

## Voices
Endplate VO: Google Cloud TTS hi-IN Chirp 3 HD, generic synthetic voices (not a clone or imitation of anyone):
female hi-IN-Chirp3-HD-Pulcherrima (L1, "natural healing"), male hi-IN-Chirp3-HD-Alnilam (L2, "second opinion").
VO text (LONG_SPEC.md, changed 23 Nov per ENDPLATE_VO.md):
- L1: क्या आप अपनी सेहत के लिए आयुर्वेद और प्राकृतिक तरीकों को अपनाना चाहते हैं? अब जीना सीखो हिम्स की वर्चुअल ओपीडी में, घर बैठे, वीडियो कॉल पर हमारे आयुर्वेद डॉक्टरों से बात कीजिए। डॉक्टर आपकी बात ध्यान से सुनेंगे, आपकी दिनचर्या और खान-पान समझेंगे, और आयुर्वेद के नज़रिए से आपको मार्गदर्शन देंगे। नीचे दिए लिंक पर क्लिक करें और अपनी वीडियो कंसल्टेशन बुक करें।
- L2: अपनी सेहत को लेकर एक दूसरी राय चाहते हैं? जीना सीखो हिम्स की वर्चुअल ओपीडी में, आयुर्वेद डॉक्टर से घर बैठे वीडियो पर विस्तार से बात कीजिए। अपनी रिपोर्ट्स और अब तक का अनुभव साथ रखिए; डॉक्टर आपकी पूरी बात समझकर आयुर्वेद के अनुसार सलाह देंगे। नीचे दिए लिंक से आज ही अपनी वीडियो कंसल्टेशन बुक करें।
(Verified word-by-word by Chirp transcription when the WAVs were made: ads/vopd/vo/verify.json.)

## Checks
- ffprobe: all 4 files have video + AAC 48 kHz stereo audio and run 5:04.6–5:05.5 (inside 5:00–6:30). Masters 1920x1080 / 1080x1920.
- Frames: one frame from the middle of every segment plus 2 endplate frames per file were extracted and looked at.
  - Captions are readable with no tofu; the hook overlay is on s01; the lower-third is on s10–s14 only.
  - No disclaimer footer.
  - No lab reports, prescriptions, phone numbers, prices or URLs on screen (the nY promo banner and the cUD burned-in caption are cropped out).
  - Endplate card text matches LONG_SPEC.md and the 👉 renders.
- Vertical face QC (qc.py check over the whole edit, endplate excluded): PASS for both vertical files. All 16 segment-level QCs PASS (render.py, or the manual-crop re-check).
- Loudness (ebur128): about -14 LUFS integrated (two-pass loudnorm to -14, then a peak limiter); true peak listed per file in the table above.
- Voice-over: L1_F.wav and L2_M.wav are the exact files from ads/vopd/vo/ (durations 22.26 s / 19.31 s match).
  Their Chirp back-transcription (vo/verify.json) has no missing words against the LONG_SPEC.md text. A listen-check was not possible.

Frame sheets (one frame per segment + 2 endplate frames, in edit order): sheet_landscape_F.jpg, sheet_landscape_M.jpg, sheet_vertical_F.jpg, sheet_vertical_M.jpg.
