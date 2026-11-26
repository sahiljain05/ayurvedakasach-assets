# Rescan v2: caption-only candidate windows (26 Nov 2026)

User-approved, caption-only rescan of the 19 lives/webinars re-queued as "todo (rescan v2; ...)" in live_videos.txt, judged against RULES_V2.md. Nothing was downloaded or rendered. Source: the captions already cached in /opt/aks/work (YouTube auto-captions).
- **Total: 77 candidate windows in 14 videos.** 69 are in Hindi and 8 in English (Rgl6csDRu-s, guest doctor). Confidence: 11 high, about 44 med or med-high, the rest low or low-med.
- **0 candidates:** Zi6ajp0wyag and wXNi7FqgUdg (facilitator sessions, Acharya Ji never speaks), wMWqLzDPvrM, and EhqZQRLN3gs (course/franchise pitch throughout).
- **Not scanned:** piAh_rqTIjM. No captions are cached (the 23 Nov scan used a vidIQ transcript that wasn't saved), and vidIQ has 2 credits (a transcript costs 5).
- **Captions don't show who is on screen.** Speaker attributions are guesses from the text. Every window still needs the normal pipeline: Chirp transcript, caption cleanup, tighten.py (cuts listed below), speaker-crop, face QC, contact sheet, and the compliance re-check.
- **Times:** start-end are source seconds. A leading "~" means approximate (qkxfiVkCPdU and E3q5jo_LgAg have long caption lines). "after cut" lengths assume the listed cut.

## Reviewer flags (fix before use)
- **66vdFPtAx8M 5222.9-5336 (elaichi + laung powder for acidity):** a specific herb dosage for a condition, which RULES_V2 still bans. Use it only without the quantities, or drop it.
- **ab5GeF8IBM4 671.0-854.4:** 183 s raw. It needs the listed cut so it ends at 176 s or less, or tighten.py will refuse it.
- **oAUTKUqdZzU 2794.3-3015.0:** 221 s raw, about 155 s after the listed cut. It only works with that cut.
- **Duplicates, pick one of each pair:** GPFnAqxDBWM 3718-3792 and 6gqkQqlSAFo 584-685 (fake milk); oAUTKUqdZzU red-light ad / wedding / Japanese barfi; ojYoAQfyj60 rows 1 and 4.
- **Rows marked low** (patient overlap, pitch-like context, unverified figures) need a strict compliance re-check on the real transcript, or should be skipped.

## Can the windows be downloaded now? (checked 26 Nov 2026 ~23:20 IST)
- **yt-dlp: no.** YouTube answers "Sign in to confirm you're not a bot" for this VM. Also, yt-dlp 2026.10.26 rejects the installed node 20.19.2 as a JS runtime ("unsupported"), so `--js-runtimes node` doesn't take effect.
  - **To fix:** (1) a cookies file from a logged-in YouTube browser session (`--cookies`, needs the user's account and approval), or wait for the block to lift; and (2) install deno, or a node version this yt-dlp supports, for the JS challenge.
- **vidIQ import: partly.** Imports are free, but the cap is 299 MB (a 78-min webinar was about 349 MB on 23 Nov).
  - **Might fit:** 6gqkQqlSAFo (56 min), _hZOPMvvQr4 (54 min) and E3q5jo_LgAg (85 min, imported once before).
  - **Will not fit:** the other 11 videos (1.5-2.8 h).
  - **Caveat:** vidIQ returned 360p files for several pool videos today, and those are skipped as too low-res.


## 66vdFPtAx8M: Kidney Health special webinar (2:47:06)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| 66vdFPtAx8M | 1236.8-1367.1 | 130 | Simple diet correction: eat only when hungry, cut animal foods and adulterated paneer/milk (FSSAI fake-paneer stat), no late dinner after sunset | Acharya Ji + Dr. Ish (1300-1341 is Dr. Ish; speaker? for 1236-1300, likely Acharya Ji) | none. Start after 1219-1236 ("goli capsule... kaam nahi karta"), which implies medicine doesn't work | med |
| 66vdFPtAx8M | 2174.8-2216.6 | 42 | "Don't just have a baby, have a healthy baby": plan 3 months ahead, sperm/egg strength comes from diet and lifestyle | Acharya Ji | none. Stop before the "IVF likh do" promo at 2216.6 | high |
| 66vdFPtAx8M | 3006.1-3048.2 | 42 | Why does a 28-year-old get blood cancer? "36 causes": dairy/eggs/non-veg, late sleep and waking, heavy curtains blocking sunlight, water before meals, bread, toothpaste, plastic brush; detox your body | Acharya Ji (answering a patient) | 3011.3-3014.9 (patient's reply "doctors said maybe genetic") | med |
| 66vdFPtAx8M | 3336.0-3508.1 | 172 | A tumor is basically "kachra" (undigested food or toxins that never left the body); childhood boils were the body clearing waste; microplastics from toothbrushes and hot food in Zomato/Swiggy plastic boxes; don't wait for disease, detox | Acharya Ji (patient Siddharth says "haan haan" over it; name only before 3336) | optional ~3401-3410 (vaccination/antibiotics line, a reputational risk but not a hard line). Patient "haan haan" overlaps can't be cut cleanly | low |
| 66vdFPtAx8M | 5222.9-5336 | ~95 after cut | Kitchen remedy for acidity, sour burps and heaviness: roast 10 small elaichi + 10 laung, powder, lick a pinch on an empty stomach (sublingual logic) | Acharya Ji | 5273.1-5290.9 ("in 5-6 days your acid pill will stop / pink pill or syrup..."): hard line 2. Resume at "subah-subah aapne vo powder..." | med |

Why the rest fails: it is mostly host intros and spoken phone numbers (7710371037, 9882789827), camp, hospital, IVF, NHP-course and product/ghee promos. There are many named patient calls and testimonials (Priyank Tandon, Ashwini Upadhyay, Bharti Singh, Aanya, Indira Sharma, Sujeet Pandey). There are constant cure claims ("theek ho jayega", "70% pathri nikal jati", "8-14 din mein inhaler chhoot jayega"). There are explicit hard-line-2 statements: no biopsy/FNAC/PET (6915-7291), stop dialysis/chemo/BP/blood-thinner/TB/sugar meds. The green-juice protocols for fibroids/tumors/hemoglobin are herb dosages tied to disease cure claims. Dr. Meghna's gut-root talk (236-528) is host-only.

## Zi6ajp0wyag: HiiMS Meerut live, 22 Nov (1:55:02)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| (none) | | | | | | |

Why it fails: the whole video is a facilitator-led session (chair-pose game, dance, liberation kriya, bhastrika, sound bath, mantra, gratitude writing). Acharya Ji never speaks. The facilitator is very likely Dr. Yashika Jain (same script as 9msc0XUtuLY), but she isn't credited in this video. The only educational bit (anger stored in the liver, 943-1135) repeats the 9msc0XUtuLY window below and has "heal without any medicine" lines (2061-2084, 1596).

## wXNi7FqgUdg: HiiMS Meerut live, 22 Nov morning (1:44:31)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| (none) | | | | | | |

Why it fails: the same facilitator/sound-healer format (partner games, dance, writing-out-emotions with songs, breathwork, sound bath). Acharya Ji is not on mic. The short psychosomatic/mental-hygiene talk (2055-2252) is facilitator-only and includes "80% of diseases need no medicine (WHO)". Off-mic staff chatter (2317-2402) admits that stat is unsourced. It also says "this session can correct your chronic disease" (654).

## 9msc0XUtuLY: Live with Dr. Yashika Jain & Dr. Sonali Garg (2:03:35)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| 9msc0XUtuLY | 948-1051.3 | 103 | Ayurveda: "vata hi chalayman, pitta pangu, kapha pangu". No machine measures vata, only nadi pariksha does. Mental disorders start with vata imbalance, emotions are its biggest cause, so fix the mind first | Dr. Yashika Jain (credited guest, Ayurvedic doctor) | none | med |
| 9msc0XUtuLY | 603-743.4 | 140 | Suppressed anger hits the liver (indigestion, fatty liver, skin issues). Suppressed tears raise cortisol, leading to insomnia, BP, irritability and isolation | Dr. Yashika Jain | none. Audience hand-raise prompts stay in. Her "yeh research keh rahi hai" lines are unsourced, so the caption must not repeat them | low |

Why the rest fails: most of the video is games (chair pose, balloon, naagin dance, clap focus), emotion-writing with songs, breathwork, a sound bath and mantra. Her claims are hard line 1: "35,000 healed without any medicine", "90% patients cured by panchakarma and sound alone", breast tumor shrank 30%, "blockages removed", students "cure" chronic liver disease and constipation in 2-3 sessions (2591-2842). The psychosomatic intro (363-452) overlaps the anger window and leans on an unsourced "90% of doctors say" stat. Dr. Sonali Garg doesn't appear clearly in the captions.

## ab5GeF8IBM4 — Navi Mumbai Health Camp 17–18 Nov (Meet Acharya Manish Ji)

Speakers: 0–~2100 s is Dr. Eesh (HiiMS senior doctor, BAMS MD PhD, introduced by name at 2556 s and 6366 s) giving a talk at the camp. From ~2700 s a host speaks ("मैं, डॉक्टर ईश और आचार्य जी एक गाड़ी में थे"), and the 2750–4500 s monologue may be the host or Acharya Ji. Acharya Ji is clearly speaking from ~4527 s ("मैं लेट हो गया", patients say "मनीष जी नमस्कार" at 6445 s). The burned-in ticker that caused the earlier skip still has to be checked on the contact sheet for every clip.

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| ab5GeF8IBM4 | 176.9-287.7 | ~100 | Eat only when hungry, no exceptions; skipping a no-hunger office breakfast is better than eating it | Dr. Eesh | 218.0-225.2 (seating chatter "डॉ साहब प्लीज हैव अ सीट"), 237.9-241.7 (chatter) | med |
| ab5GeF8IBM4 | 349.0-519.9 | ~159 | Hunger makes the body "eat" its diseases: Ayurveda shloka plus the 2016 Nobel (Ohsumi, autophagy); every religion's fasting; don't overdo it; find your own type of fast | Dr. Eesh | 474.8-486.3 ("आपका यू-टर्न शुरू ... हीलिंग शुरू हो गई", sounds like reversal) | high |
| ab5GeF8IBM4 | 671.0-854.4 | ~175 | Why do we age and fall ill? Theories of ageing; the free-radical theory is in our control; overeating and stress create free radicals | Dr. Eesh | 753.8-762.0 (aside about phone calls); if over 176 s after tighten, start at 762.0 instead (~92 s) | med |
| ab5GeF8IBM4 | 874.0-987.9 | ~114 | "97% of your worries are imaginary", but the BP and hormones they cause are real (5-year friend story) | Dr. Eesh | none | high |
| ab5GeF8IBM4 | 1256.6-1327.5 | ~70 | Ayurveda's basic mechanism of disease: weak metabolism/digestion, wrong absorb-vs-excrete, toxins build up; diet prevents it, panchakarma removes it | Dr. Eesh | none | high |
| ab5GeF8IBM4 | 1655.7-1812.4 | ~155 | What the 5 panchakarma actions are (any nearby centre, no need to come here); once a year keeps you healthy; do it before illness; "karz aur marz ko chhota mat samjho" | Dr. Eesh | 1764.0-1766.0 ("आ जाइए, इधर आ जाइए") | med |
| ab5GeF8IBM4 | 4362.8-4425.1 | ~62 | The protein myth: where do the elephant and horse get protein? Chana was only for horses on journeys, in the jungle they eat grass | speaker? (host or Acharya Ji; a patient may be on stage, check the crop) | none | low |
| ab5GeF8IBM4 | 5401.2-5481.0 | ~80 | Six conditions before drinking cow milk (desi humped cow, grazing, no hormone/antibiotic shots, sunlight, natural calving, no sprayed fodder); otherwise coconut/almond/peanut milk | Acharya Ji | none | med |
| ab5GeF8IBM4 | 6020.3-6070.4 | ~50 | "We are all unplanned babies": Ayurveda says prepare 3 months before conceiving (diet, lifestyle, yoga, happiness) for a healthy child | Acharya Ji | none | med |

Why the rest fails: the patient testimonials and case parades (Ganesh ji blood cancer, Hiral liver, Priyank AML, Anya brain tumour, Raju ji) come with "बिल्कुल ठीक हो गए"/"reverse" cure claims and anti-chemo, surgery, biopsy and medicine lines ("दवाई नहीं चाहिए", "कीमो के लिए मना करते हैं", "dialysis band", "शुगर-बीपी की दवाइयां छुड़वाई"). Other parts are hospital, panchakarma-for-attendants and insurance/advocate promos, the patient Q&A (identifiable names and room numbers) and setup/anthem/chatter. Also dropped: the IVF/DNA/milk-sterility jibes, the religion comparison in the vajrasana section and the sudden-death video montage.

## qkxfiVkCPdU — Special webinar on health and scientific Ayurveda

Speakers: Dr. Pratibha hosts. Dr. Eesh (named) gives the Ayurveda basics at ~416–1600 s and short explanations later. Acharya Ji joins at ~1590 s and runs case parades and patient calls; Dr. Shailendra Bhardwaj closes. The captions come in ~16 s blocks, so starts and ends marked "~" are mid-block estimates and need checking against word timing.

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| qkxfiVkCPdU | ~459-561 | ~102 | "Putting pills in your mouth isn't treatment": the 4 pillars of Ayurveda (diet as super-medicine, lifestyle, some medicines, panchakarma); overeating, heavy dinner after 7 pm, eating without hunger and too much animal food are the biggest causes of disease | Dr. Eesh | none (start at "अब आयुर्वेद है क्या?", the last words of the 447 block) | med |
| qkxfiVkCPdU | ~1390-1441 | ~51 | "You're racing towards disease, and diseases are in a bigger hurry": heart attacks at 20, cancer at 25, type-2 diabetes at 15; don't wait until you're sick | Dr. Eesh | none (start at "आप बीमार पड़ने की तरफ भागे जा रहे हो"; end after "इफेक्टिव नहीं हो पाएगा") | high |
| qkxfiVkCPdU | ~1499-1562 | ~63 | "Rogah sarve api mande agnau": every disease comes from weak agni and overeating; make fewer toxins (fasting/autophagy) and remove them (panchakarma) | Dr. Eesh | none (end at "पंचकर्म के द्वारा", before the green-juice "reverse" claim at ~1586) | med |
| qkxfiVkCPdU | 8616-~8673 | ~57 | Why autoimmunity: cells mistake our own organs for enemies when we move away from nature (lights at night, AC, the 2017 Nobel on circadian rhythm); walk barefoot, honour day and night | Dr. Eesh | none (end at "बॉडी में कन्फ्यूजन कम होगा", before "ऑटो इम्युनिटी रिवर्स होगी") | med |
| qkxfiVkCPdU | ~8783-~8890 | ~107 | "No disease comes overnight": ama builds up over years; diet stops it, panchakarma removes it; service the car before it breaks down; real panchakarma is vamana/virechana/nasya/raktamokshana/basti, not just massage | Dr. Eesh | none (start at "कोई बीमारी रातोंरात नहीं आती है"; end before "थैंक यू वेरी मच") | high |

Why the rest fails: Acharya Ji's whole segment (~1590–8925 s) is hard lines. It has celebrity and patient testimonials (Ashwini Upadhyay, Bharti Singh's mother "insulin band in 4 days", Anya, Priyank, Happy Chawla fibroids, Indira breast cancer "gaanth khatm in 10 days"). It has lines against surgery, biopsy, chemo and medicine ("biopsy kara ke mat aao", "chemo band kyon nahi", "dawai se nahi hoga") and "blood cancer = acidity, make it alkaline" cure claims. It is also full of spoken name/mobile-number requests, centre, price, test and insurance promos, product kits (Dr. Maa/Dr. Pa, Sea Buckthorn juice) with dosages, and the webinar schedule. Dr. Pratibha's opener attacks transplants and immunosuppressants and introduces testimonials. Dr. Bhardwaj's close has "jad se khatm" and "koi problem nahi aayegi". A ~694–851 s Dr. Eesh panchakarma explainer was also clean, but it was left out because it makes the same point as the 8783 clip (and the ab5GeF8IBM4 panchakarma clip).

## HqdnG2TSE5o (Cancer/Liver/CKD special webinar, Hindi)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| HqdnG2TSE5o | 3056.0-3126.2 | 70 | What vaman is: herbs given according to prakriti, routine vomiting only clears the food pipe while classical vaman pulls hidden toxins, plus dhoopan for the ear and nose; virechan explained (Acharya Ji narrating his own vaman video) | Acharya Ji | none (the clip starts after the staff line "वीडियो चलने दे" at 3052; the video shows actual vomiting, so check the frames) | med |
| HqdnG2TSE5o | 3563.1-3612.8 | 50 | "बीमारी के नाम में कुछ नहीं रखा": allopathy has 10,000 disease names and 150 kinds of blood cancer, while Ayurveda sees one "रक्त में अमलता"; call it kachra, tumor, cyst or gaanth | Acharya Ji (patient only says "जी प्रभु") | none. End before 3613.3: the next lines "अंदर से ही ठीक हो जाएगा" (3620.7) are a hard-line cure claim | med |
| HqdnG2TSE5o | 2792.3-2836.8 | 37 after cut | "Every vehicle needs a service, and so does every person, child to elder: that service is Panchakarma" | Acharya Ji + patient replies | cut 2806.4-2813.1 (patient's own answer). Stop before 2836.8: the Trehan clip follows, and 2913-2922 "इस जन्म में डॉक्टर की शक्ल भी नहीं देखनी पड़ेगी" is a guarantee | low |
| HqdnG2TSE5o | 2668.6-2702.5 | 34 | "यार दूध जहर है": milk, curd, paneer, egg and non-veg; cows no longer graze on herbs, artificial insemination | Acharya Ji (the 4 s question is from an anonymous caller) | keep the anonymous question audio, or show it as on-screen text (without it the clip is only 29 s) | low |

Why the rest fails: about 0-1400 s and 1494-2500 s are the host (Dr. Meghna) only: chat roll-call with patient names, a support phone number, named patient testimonials (Priyank Tandon, Bharti Singh's mother, Ashwini Upadhyay: "dialysis बंद हो गई", "गांठ गायब"), camp/hospital promos and booklets saying biopsy, mammography and medicines cause harm. Nearly every Acharya Ji answer in the patient calls (2586-7520 s) crosses hard line 1 or 2: "बायोप्सी मत कराना", "कीमो नहीं कराना / 98% कीमो से मरते हैं", "steroid लोगे तो किडनी फेल", "शुगर/BP की दवाई मत देना", "डायबिटीज रिवर्स करा देंगे", "ठीक हो जाओगे". Callers are named and many give their city. The rest is centre/doctor routing, a kit sale (Doctor Maa/Pa), a store.jeenasikho.com product pitch, free tests and the Rs 1000 FibroScan promo. The lifestyle lines are under 20 s and sit inside disease calls.

## oAUTKUqdZzU (HiiMS Meerut camp live, Hindi)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| oAUTKUqdZzU | 2794.3-3015.0 | 155 after cut | Red-light "switch off the engine" ad story: restarting the car burns more fuel than idling saves. In the same way, even one small bite of barfi starts the whole digestive machine, so stop eating and sipping all day: drink when thirsty, eat when hungry | Acharya Ji | cut 2811.8-2877.2 (audience guesses, Devesh Singhal named, gift and mic banter). Optional: 3000.5-3002.4 "किडनी फेल भी होएगी भैया" (scare line about drinking 3 L of water) | high |
| oAUTKUqdZzU | 3105.0-3240.3 | 135 | Nobody cooks pulao by adding rice every 15 minutes, yet at a wedding we graze from 8 pm soup to 12:15 kulfi, so of course the liver suffers. Vow: never eat or drink standing, sit down to eat | Acharya Ji | optional 3203.3-3217.4 (banter with an audience member) | med |
| oAUTKUqdZzU | 3051.7-3105.0 | 53 | The Japanese live longest: offered birthday barfi, a Japanese person wraps it in a napkin and eats it only at mealtime. "जब ढक्कन खोलो तभी डालो" | Acharya Ji | none. Same point as the two rows above, so use it as a short 30-60 s alternative and not alongside them | low |
| oAUTKUqdZzU | 4219.6-4289.1 | 62 after cut | Why eat sitting in vajrasan on a low chowki: straight back, the stomach is not compressed, blood stays with digestion. Japanese, Chinese, Korean and Thai people and Muslims all eat this way | Acharya Ji | cut ~4265.7-4269.5 (word-level: "ना डायबिटीज होगी, ना ब्लड प्रेशर होगा", a hard-line-1 "won't happen" claim). Keep "...ना एसिड बनेगा। जापानी..." | med |
| oAUTKUqdZzU | 5211.9-5391.8 | 165 after cut | Water and meals: sip water during a meal (it clears the tongue, more saliva, better digestion), but not just before or after (it dilutes the digestive juices). Ends on Acharya Ji's Chanakya shloka: "भोजन करते हुए पानी अमृत, अंत में विष" | Dr. Ish Sharma (introduced on stage as BAMS MD PhD) + Acharya Ji from 5354 | cut ~5273.5-5288.1 (word-level, "अगर आपको लगता है... साहिल ने हमको सिखाया... यात्रा शुरू हो चुकी है"), needed to get under 176 s | high |
| oAUTKUqdZzU | 1461.2-1596.0 | 129 after cut | Morning routine and Plate One: warm water instead of tea, chew raw turmeric, ginger or curry leaves on waking, eat between 8 am and 8 pm, 500 g (or 250 g) of fruit before breakfast, cheap seasonal fruit because it is chemical-free | Dr. Neha (staff doctor, introduced on stage; not Acharya Ji) | cut 1485.7-1491.8 ("हीमोग्लोबिन लेवल कभी गड़बड़ नहीं होगा", a "kabhi nahi" claim) | low |

Why the rest fails: 0-1000 s are the host/facilitator: rituals, a cancer-gene talk, autophagy "कैंसर सेल्स खा जाते हैं" and camp promotion. 1000-2380 s are Dr. Neha's diet talk with disease-cure lines (ash gourd "वरदान है कैंसर के लिए", green juice dissolving gaanth, "डायबिटीज, लीवर रिवर्स"). About 3290-3890 s and 4300-5200 s are guest and patient testimonials (named, "मेडिसिन कम करा दी", "no medicine"), the Quran/Patanjali eating-postures segment led by staff and guests, NHP course sales (Rs 12,000) and a spoken phone number (91142 91642). 5928-6155 s is a women's green-juice remedy with guarantees ("कभी रसोली/PCOD नहीं आएगी", "80-90% सॉल्व", cancer "खत्म"). 6200-8920 s is a group meditation and hugging exercise that ends with "ना कभी किडनी खराब होगी... हार्ट अटैक नहीं".

## Rgl6csDRu-s (JANA US webinar; Dr. Ish Sharma speaks English, Acharya Ji's Hindi parts are garbled in the en captions)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| Rgl6csDRu-s | 924.9-1039 | 114 | [EN] Why we age: oxidative stress is the one theory of ageing we control, and overeating and stress are its biggest sources. 97% of stresses are imaginary, yet the cortisol is real. "Staying hungry is golden" | Dr. Ish Sharma | none (end mid-caption after "golden", before "now we come to the next slide") | med |
| Rgl6csDRu-s | 1383.4-1513.5 | 130 | [EN] "We work very hard to earn one disease": stress, overeating, late eating, microplastics. Being reactive is too late, because atherosclerosis starts with foam cells at age 10 | Dr. Ish Sharma | none | med |
| Rgl6csDRu-s | 3232.2-3369.8 | 138 | [EN] Ayurveda's view of autoimmunity: detaching from nature (artificial light, AC, blackout curtains) confuses circadian and circannual genes, and the body attacks itself. Reconnect: sun, seasons, barefoot on grass | Dr. Ish Sharma | none | med |
| Rgl6csDRu-s | 3572-3687.0 | 115 | [EN] The gut is the most important organ: detox the gut and you need not detox each organ. Panchakarma steps explained: vaman, virechan, herbal basti | Dr. Ish Sharma | none (start word-level at "So which is the most important organ") | med |
| Rgl6csDRu-s | 633.9-759.5 | 126 | [EN] "Food is super medicine" (aahar mahabhaishajya). More people die of overeating than starvation, so before asking what to eat for diabetes, ask whether to eat at all | Dr. Ish Sharma | none. Stop before 774: "obesity/fatty liver/tumors/diabetes would go away" is a cure claim | med |
| Rgl6csDRu-s | 2656.2-2701 | 45 | [EN] Mindful eating: eating while watching TV, on the phone or over business lunches means less digestive juice and poor digestion | Dr. Ish Sharma | none | med |
| Rgl6csDRu-s | 2813.0-2866.6 | 54 | [EN] Dinner timing: before sunset, about 7 pm; Plate One soup or salad first; make dinner the lightest meal, "leave your dinner for the enemies" | Dr. Ish Sharma | none | med |
| Rgl6csDRu-s | 4214-4284.2 | 70 | [EN] Every healthy change brings teething problems (getting up at 6 instead of 8; learning to ride a bicycle): don't give in, and in a week it becomes the new normal | Dr. Ish Sharma | none (start word-level after "they should ignore that sickness") | med |

Why the rest fails: the whole lecture is English. Acharya Ji's Hindi segments (about 318-460, 1040-1340, 1560-1830, 2040-2250, 2990-3160, 3380-3530 s) are unusable in the en captions and contain cancer-free, insulin and dialysis talk. The Q&A on taking Ayurveda with allopathy (1859-2011 s: taper or withdraw metformin, insulin and BP drugs, "countless patients off medicine") and on GLP-1 (4083-4180 s: "the more you go for GLP1 the more you are disowning your health") cross hard line 2. 774-817 s and 2249-2300 s claim fasting makes tumors and diabetes "go away". The rest is intros and thank-yous, garbled slide talk, or garbled thyroid/kidney Q&A.

## ojYoAQfyj60 (All Disease Webinar LIVE)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| ojYoAQfyj60 | 817-861 | 44 | "Getting sick takes effort": modifiable vs non-modifiable factors; the two to fix are stress and overeating (no eating without hunger) | Dr. Ish (credited guest, MD PhD Ayurveda) | none (end before "...jo ban gaye unko nikaalne ke liye panchkarm hai" at 861) | med-high |
| ojYoAQfyj60 | 1069-1106 | 37 (~34 after cut) | Stop needless worry: most of our worries are imaginary, stress raises cortisol and BP | Dr. Ish | 1086-1089 (aside "Dr Meghna woh clip bhi dikha sakte hain"); end before "overeating chhod dein, panchkarma karvayein" | low (unverified "97% research" figure; same theme as row 1, so pick one) |
| ojYoAQfyj60 | 2068-2133 | 65 (~59 after cut) | "Service your body every 6 months": detox/panchakarma as prevention; heart attack, BP, sugar complications are now common; build strength and immunity | Acharya Ji | 2092-2098 ("is janam mein agar beemar nahi padna... varna hairaan ho jaoge": borderline never-get-sick promise) | low (sits inside a cancer-patient answer; reads as a panchakarma pitch) |
| ojYoAQfyj60 | 4721-4751 | 30 | "Our body is not made to fall ill; we get sick through our own known and unknown mistakes" | Acharya Ji (patient "hmm" in the background) | none | med (same idea as row 1; keep only one of the two) |
| ojYoAQfyj60 | 4529-4581 | 52 | Samosa example: a food is not healthy just because it gives you no gas right away; gluten/wheat sensitivity is the body warning you | Acharya Ji | none (start after the "celiac koi disease nahi" line at 4518) | med |
| ojYoAQfyj60 | 5853-5942 | 89 | "Can science make one eye, ear or hair?" The body is intelligent; a tumour forms for a reason (known or unknown mistakes) | Acharya Ji + anonymous patient answering (no name in window) | none (end before "woh theek kar denge, reverse ho jayega" at 5942) | low |

Other parts fail: most of the run is patient Q&A with named callers, cities and diseases (cancer, CKD, type 1 diabetes, fibroid, brain tumour). These answers carry hard lines: advice against chemo, biopsy, surgery and insulin ("insulin nahi lagana", "kuch mat karao"), reversal and cure claims ("jad se khatm", "90% reverse", "theek ho jayenge"). There are also patient testimonial videos (Ashwini Upadhyay, Priyank, the badminton girl), centre, insurance, kit and juice promos, store.jeenasikho.com, a spoken support number (7710371037) and a long CNH/NHP course sales and Dr Maa/Pa package segment. The death-compilation segment is also out. Dr. Meghna's agni/toxin explanation (354-521, 6837-6880) is host-only and also contains "jad se khatm / panchkarma only option".

## EhqZQRLN3gs (Building a healthier India through natural healing)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| (none) | | | | | | |

Other parts fail: this is an NHP/CNH course and franchise sales webinar from start to finish (fees ₹9,600/₹33,600, ₹1,000 token, ₹1 lakh franchise, 15%/10% referral commission, spoken booking number 91142 91642, "bada paisa" earning pitch, testimonial videos). Acharya Ji only appears briefly for logistics and franchise talk. The only general-health teaching is from the host Dr. Rajshree (fire-alarm analogy 443-660, swasthasya swasthya rakshanam ~1260). It is host-only, and it leads straight into anti-medicine lines: daily BP/sugar pills are "sweet poison", don't "pop pills" (hard line 2). HP Vashishth's BP-drug-cascade story (2980-3055) is a non-doctor promo with the same problem.

## 9zgouWUD-Bk (Dr Yashika Jain Sound Healing Live)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| 9zgouWUD-Bk | 116-200 | 84 | Two pillars of health, dinacharya and ritucharya (6 seasons, change diet every 2 months); keep digestion strong enough to "digest stones"; after a heavy night fast in the morning: "langhanam param aushadham" | Dr. Yashika Jain (credited guest doctor) | none (start after the "you never ask allopathy for a guarantee" lines; end at "fasting hi sabse badi aushadhi hai" before the pills/dependency lines at ~200) | med-high |
| 9zgouWUD-Bk | 1961-2027 | 66 | Suppressed anger doesn't go away: Ayurveda links held-in anger to the liver, manda agni, skin and BP problems; emotions need shodhan, not just control | Dr. Yashika Jain | none | med (strong causal claim; group shouting exercise starts after 2027) |
| 9zgouWUD-Bk | 1877-1928 | 51 | Why panchakarma takes about 21 days: doshas hide deep in the tissues and are first drawn back to the stomach/intestine, then the main procedure (pradhan karma) removes them | Dr. Yashika Jain | none | med |
| 9zgouWUD-Bk | 6097-6221 | 124 | "Diseases don't come from America or Japan": overused liver, unrested kidneys; the 8-litre water myth: drink when thirsty, eat only when hungry; Japan 84 vs India 66 life expectancy; "whose fault is it?" | Acharya Ji | none (end at "kiski galti hai?" before "zaroori nahi ilaaj ka tareeka sirf dawai ho" at 6224) | med-high (life-expectancy figures need a fact check before captioning) |
| 9zgouWUD-Bk | 6234-6273 | 39 | Release, don't bottle up: talk to someone; if you can't, lock the door and cry or shout in front of a mirror, but get it out | Acharya Ji | none (end before "rone hansne se naadiyan balance... clot theek ho jayega" at 6273+) | low-med (overlaps the emotional-release row 1961-2027) |
| 9zgouWUD-Bk | 7339-7450 | 111 (~56 after cut) | Don't cry and talk negative in front of a seriously ill family member; it lowers their morale and makes healing harder | Acharya Ji | 7369-7426 (the "bhugatne do saale ko", liver/kidney-fail mockery and the doctor-reply aside); end before "jiska dar nikal gaya woh nahi marta" at 7450 | low-med |
| 9zgouWUD-Bk | 7774-7852 | 78 (~63 after cut) | Stay happy every minute: let others carry the tension, don't fill your mind with garbage, hear with one ear and let it out the other; tension will make you ill | Acharya Ji | 7805-7820 (aside about this session: "main do baar bol ke gaya tha... video hai mere paas") | med |
| 9zgouWUD-Bk | 7913-7960 | 47 | "Enema is naturopathy; Ayurveda has basti": different bastis for different organs, nasya ("nasa hi shiraso dvaram"), raktamokshan/leech therapy | Acharya Ji | none | low-med (starts as a reply to a participant; a quick explainer) |

Other parts fail: the 9-minute emotional-release "kriya" is pitched with cure and guarantee claims ("meri guarantee hai shugar/BP yahin chhod ke jaoge" 2533-2547; the released chemical "beemariyon ko theek karne lagta hai" 2666-2685). There are long stretches of games, dance, national anthem and music with no speech. The wrist-artery/suicide body-intelligence story (6383-6540) is self-harm content. The heart-attack home first aid (ginger, chilli water, calf pounding, 6724-7200) is unproven emergency advice with "ambulance ki zaroorat nahi padegi" and "99%" claims. Then come the death videos and the "fear makes you do biopsy/dialysis/transplant, you sign for your death" segment (7459-7560, hard line 2). "Vaman-virechan every 3 months, is janam mein beemar nahi" (7864-7888) is a guarantee plus panchakarma promo. The gratitude-writing exercise (8180-8650) is facilitator-only.


Times are source seconds. For E3q5jo_LgAg each caption line spans about 15-20 s, so starts and ends marked "~" are estimated inside a line. Check them on the waveform before cutting.

## btp7a9t_vs0

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| btp7a9t_vs0 | 455.4-522.2 | 67 | Disease doesn't come overnight: heart-artery plaque starts at age 10-12, so diet correction matters | Dr. Ish (named HiiMS senior doctor) | none (ends on "panchakarma karwana aavashyak hai", which is general; optional trim at 514) | med |
| btp7a9t_vs0 | 580.5-618.0 | 38 | "97% of your stresses are false": stress feeds every disease (vishado roga vardhananam) | Dr. Ish | none | high |
| btp7a9t_vs0 | 749.3-895.6 | 146 | Why we fall ill: mandagni/weak metabolism, toxins settle in tissues; never eat without hunger, fasting/autophagy | Dr. Ish | none ("100% bimariyan mandagni se" is a cause statement, not a cure claim; keep the caption from saying "100%") | med |
| btp7a9t_vs0 | 980.4-1062.5 | 82 | What real panchakarma is (not just massage/shirodhara): vaman, virechan, basti, nasya, raktamokshan | Dr. Ish | none (stops before the "maut ko harana" line at 1062.5) | low |
| btp7a9t_vs0 | 3553.2-3588.7 | 35 | Most diseases come from calorie overload; more people die of overeating than hunger, so fast with guidance and eat only when truly hungry | Dr. Ish | none | med |

Why the rest fails: most of the webinar is patient testimonials and identifiable patients (Priyank Tandon, Anya, Indira Sharma, Ashwini Upadhyay, Bharti Singh's mother, dialysis patients); anti-chemo, anti-biopsy and anti-surgery talk ("biopsy/PET/mammography mat karana"); cure and reversal claims; juice recipes with quantities for tumours, liver and jaundice; a product plug (Can Care, jeena.com); hospital, centre, insurance and camp promos; spoken phone numbers. Acharya Ji's own segments are all in these categories. Calls 4726-6555 are patient intake with names and cities.

## wMWqLzDPvrM

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|

(no candidates)

Why the rest fails: Acharya Ji's segments are almost entirely hard-line content: anti-biopsy and anti-chemo advice to named callers ("biopsy nahi karani", "kimo band kar do"), "cancer is just your cell, fix it and it goes", "Ayurveda mein aisi koi bimari nahi jiska ilaaj nahi". There are also testimonials and identifiable patients (Priyank, Ganesh ji, Rahul, Hetal, Bharti Singh), the biopsy before/after photo slideshow, and promos for centres, the camp, the NHP course, fibroscan prices and insurance, plus spoken phone numbers. Only two parts are clean. The herbal-tea aside at 1368-1394 is about 22 s, too short. The general talk at 290-600 (body not made to fall ill, lifestyle causes, gut as second brain, mandagni) is spoken only by the host doctor/facilitator, so it is not a candidate under the rules.

## E3q5jo_LgAg

Podcast format: host Aamir Khan plus two female co-hosts ask the questions, and Acharya Ji answers. None of the windows below touch the excluded or used windows (1937-1980, 2033-2076, 3290-3420, 1945-1980, 2032-2076, 3373-3401, 3255-3284, 4397-4434). No tighter retry of those windows qualified: 4397-4434 (washing vegetables) would come out under 30 s or would need the "dudh mat piyo" and injected-lauki lines.

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| E3q5jo_LgAg | ~317-~425 | 108 | Navel as body's centre (cord, 72,000 nadis); oil in navel in winter for cracked lips and skin, sunburn | Acharya Ji (host interjections only) | none; start after the host's "ye dono kaise connected" question (~308-317) | med |
| E3q5jo_LgAg | ~455-~522 | 67 | Nobody fully empties bladder/bowel on Western seats: squat again after urinating or passing stool (UTI, prostate, piles origin) | Acharya Ji | none; end before the "Angrezon ne..." vulgar line (~522) | med |
| E3q5jo_LgAg | ~1315-~1360 | 45 | Wedding buffet 8 pm to 12 am: soup, chaat, manchurian, ice cream, paan... no wonder the liver suffers | Acharya Ji | none; start at "shaadi mein jaate ho 8 baje", which avoids the "daaru buri nahi" lines | high |
| E3q5jo_LgAg | ~1370-~1495 | 125 | Time as medicine: body runs on the sun, no digestive enzymes after 6 pm, eat between 9 am and 6 pm, 15 h gap = autophagy | Acharya Ji (host interjection on intermittent fasting) | cut ~1466-1476 (unverifiable "Nobel scientist took it from the Vedas"); end before "cancer ki gaanth... khatm kar degi" (~1495) | med |
| E3q5jo_LgAg | ~2441-2523 | 82 | Body does one job at a time: eating while dancing at dandiya (heart strain), phone in the toilet means incomplete evacuation | Acharya Ji (host question at 2418-2440 can be a text hook) | none | med |
| E3q5jo_LgAg | ~3131-~3163 | 32 | Sleep with head east/south, lie on the left side, rise via the right side, move the body before getting up | Acharya Ji | none; start after "bahut bada raaz" set-up (the hook before it at 3096-3129 has the sugar-reverse/BP-goli claims) | med |
| E3q5jo_LgAg | 3165-3250 | 85 | Heavy late meals pull 2.5-3 L of blood to digestion: elderly night heart attacks, drowsiness after chhole bhature, truck drivers' accidents after dhaba meals | Acharya Ji | none | high |
| E3q5jo_LgAg | ~4937-~5010 | 73 | Matka water vs RO ("RO strips minerals"); if you must use RO, store it in a matka with copper, then infuse with apple, cucumber, mint, amla | Acharya Ji (host question 4916-4934 as hook) | none; end at "jeevit water ban jayega", before "cancer ko bhi hara sakta hai" (~5010) | med |

Why the rest fails: the tongue-reading part (5-252) goes into hospital kidney-failure statistics. "Sarva roga theek ho jate hain" (432). The PCOD section claims "vaccination ka khel" causes internal boils and says periods give "curse power". The olive-oil liver flush (971-1160) claims fatty liver is fixed and gallstones come out, says gallbladder removal is a mistake, and promotes the free 7-day package and hospital insurance. The fever section (2541-2800) says 90% are cured in 3 hours and to avoid fever and painkiller tablets. The rest of the video has: paracetamol called "the worst medicine" and the ₹1 lakh pill challenge; "Ayurveda can stop dialysis"; the British/law/medical-mafia rant; supplements and pregnancy folic-acid advice (implies avoiding doctor's treatment); "haldi chabao, kabhi cancer nahi hoga"; buffalo milk "poison" and Jersey cow "pig cross"; "AK-47 for the British"; the diet chart with "shugar goli/insulin chhodna"; testimonials (Bharti's mother, Rajiv Thakur, Prahlad Modi, Arjun Lal Meena); "no transplant, chemo or dialysis"; the personal story with a suicide attempt and his uncle's reversal of a heart attack; hospital chain promo; IVF fraud claims; eggs and an LGBT slur; "paneer causes PCOD"; infertility "don't save the pregnancy with medicines".

## GPFnAqxDBWM (Meerut live, Diwali week)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| GPFnAqxDBWM | 3718.6-3792.3 | 73.7 | Fake paneer/milk: who supplies 5000 kg of paneer overnight? The Nirma-detergent milk factory raid near Lucknow | Acharya Ji | none (start mid-caption at "आप बोलो मेरे एक किलो पनीर चाहिए", ~3720) | med |
| GPFnAqxDBWM | 1429.1-1499.7 | 70.6 | Squat to urinate (Indian vs. Western toilet): bladder doesn't empty, which he links to prostate, sexual and knee problems | Acharya Ji | none (end after "हाइड्रोसल की प्रॉब्लम आ जाती है", ~1498) | low |
| GPFnAqxDBWM | 2697.8-2732.7 | 34.9 | Want meat? Hunt it yourself; market chicken/goat is raised on growth hormones and antibiotics, which he links to antibiotic resistance and diabetes | speaker? (likely Acharya Ji) | none (start mid-caption at "नॉनवेज खाना है तो", ~2701.8) | low |
| GPFnAqxDBWM | 2875.0-2918.5 | 43.5 | Why non-veg was fed in the past (to make soldiers fierce), and why today's injected meat harms the body | speaker? (Acharya Ji or guest doctor) | none | low |
| GPFnAqxDBWM | 4252.8-4291.3 | 38.5 | Ayurveda shloka "vishado roga vardhananam": stress makes every disease worse; don't give a disease "respect" | guest doctor (Dr. Ish / Dr. Chhabra?), speaker? | none | low |

Why the rest fails: most of the live is patient testimonials (dialysis "बंद", blood cancer, brain tumour, liver cirrhosis, "Bablu zinda hai"), and it is full of cure and anti-treatment claims. Examples: "kabhi nahi hongi" (vajrasana: 5 diseases), "ठीक हो जाएगा", fear of chemo, dialysis, transplant and biopsy, "कैंसर से कोई नहीं मरता", 60/70-90% "results". Other failures: the Hriday Care juice opening blockages, the stage-wise admission protocol and hospital promo, the stool lucky draw, audience roll-call, and banter that targets a religion. The previously tried 1318-1366 and 1777-1832 windows were not re-listed. The only nearby alternative is 1297-1362 (same curtains/AC point), and it would use the same shot, so it was not listed.

## 6gqkQqlSAFo (Lucknow live, all diseases)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| 6gqkQqlSAFo | 718.0-844.7 | 126.7 | Pancreas has a sleep time (~2 h after sunset); the late wedding-buffet timeline from soup to coffee inflames it (circadian rhythm, Nobel 2017) | Acharya Ji | none (ends before the crude "मां बहन" line at 845.4) | med |
| 6gqkQqlSAFo | 494.3-563.3 | 69.0 | Why today's cow/buffalo milk isn't the same: injections, antibiotics, artificial insemination, sprayed fodder, no sunlight | Acharya Ji | none | med |
| 6gqkQqlSAFo | 1227.9-1333.4 | 105.5 | Coconut water rules: not Nov-Feb, sip and "chew" every sip, one coconut for four people; gulping overloads the kidneys | Acharya Ji | none (the patient's question at 1221 is left out by starting at 1227.9) | med |
| 6gqkQqlSAFo | 584.6-685.4 | 100.8 | Fake milk made with Nirma detergent (Gorakhpur factory raid, Amar Ujala headline); who can supply 500 kg of paneer overnight? | Acharya Ji | 593.1-598.7 (audience "Gorakhpur se kaun aaya") | low |

Why the rest fails: it opens with fear-of-death videos framed against dialysis, chemo and stents ("स्टंट 5000 का 1.5 लाख में"). It also has the mud-pack and ajwain pancreatitis "free ilaaj" and "BP की गोली से किडनी फेल". The 8-day Panchakarma "90% की गोली बंद, मेरी गारंटी" is a cure claim plus stopping medicine. Then come the blood-cancer and Priyank chemo testimonials, the LVF patient promised "double/चार गुना पैसे वापस", the 250-bed hospital promo, the biopsy argument, and herb mL dosages. The milk injections and Nirma milk point also appears in GPFnAqxDBWM 3718-3792: use only one of the two.

## _hZOPMvvQr4 (YouTube LIVE webinar with Acharya Ji + doctors)

| id | start-end (s) | len (s) | topic | speaker | cuts | conf |
|---|---|---|---|---|---|---|
| _hZOPMvvQr4 | 1880.3-1936.2 | 55.9 | Home warning sign: check BP at 9 am and 9 pm; a night reading equal to or above the morning one means heart-attack risk | Acharya Ji (recorded Meerut segment) | none (start mid-caption at "तो मैं चार पांच बातें बता रहा हूं", ~1881) | med |
| _hZOPMvvQr4 | 2064.0-2122.1 | 58.1 (≈44.6 after cut) | Kidney tests stay normal until about 70% damage; home check comparing day vs. night urine in two bottles (day should be 4x night) | Acharya Ji (recorded Meerut segment) | 2076.2-2089.7 (free KFT test promo) | low |

Why the rest fails: it is mostly live patient calls with names and cities, each routed to a centre or Panchakarma with "ठीक हो जाओगे" / "बिल्कुल ठीक हो जाती है, ऑपरेशन की जरूरत नहीं". A guest doctor tells a stage-4 ovarian cancer caller to skip chemo. There is the free 5-test, ₹1000 fibroscan, health-card and referral-bonus promo, the Ashwini Upadhyay testimonial ("डायलिसिस बंद"), and the liver cirrhosis patient. The guest doctor's shloka segment says medicines only suppress and Panchakarma gives "समूल नाश". The night-waking "liver failure / cancer sign" and HDL segments are scare claims wrapped in the free-test promo.

