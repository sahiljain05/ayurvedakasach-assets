# VOPD full ad: Acharya Ji part + 3D b-roll endplate (user approved, 23 Nov)

## 0. Disclaimer footer removed (user decision)
The user does not want the disclaimer footer. Remove the footer requirement from SPEC.md, LONG_SPEC.md and the queued endplate-fix job (run_vopd_endplate_fix.sh): no footer text on any VOPD output. Everything else in those specs stays (no cure claims, no disease names, no stop-medicine hints, no price/number/URL on screen). L2_M.wav at 19.3 s is accepted as is.

## 1. What to make
4 full ads, 16:9 1920x1080, one per endplate:
ads/vopd/full/vopd_full_L1_F.mp4, vopd_full_L1_M.mp4, vopd_full_L2_F.mp4, vopd_full_L2_M.mp4

Structure of each:
1. Acharya Ji part, 25-40 s, from his official long-form videos (landscape source, keep landscape, no face crop needed; if the source is not 16:9, fit with blurred background).
2. 0.5 s crossfade (video and audio) into the matching endplate video ads/vopd/endplate/vopd_endplate_<name>.mp4 (26 s, already has the voiceover; use it as is, no footer).
Total length about 50-65 s.

## 2. Choosing the Acharya Ji part
- Prefer windows the short-ads job already downloaded and transcribed (reuse, don't re-download). Use Chirp only on a new chosen window, never a whole video.
- Two different segments: one for the L1 ads (natural healing: daily routine, food habits, listening to your body, lifestyle) and one for the L2 ads (why understanding a person's full routine and history matters, taking a considered opinion). Same segment for F and M of each script.
- Must start on a clean sentence start and end on a complete sentence. Strong first 3 s hook.
- Hard rules: no cure / guarantee / "jad se khatm" / "theek kar denge" claims, no disease names, nothing that suggests stopping or changing medicine, no Dr. Biswaroop footage or voice, no patient footage. If a window breaks any rule, pick another.
- Burn Hindi captions on the Acharya Ji part only, same caption style as the reels (ass, shaping=complex, Noto Sans Devanagari), bottom third. No captions on the endplate (it has its own title card).
- Small credit top-left during the Acharya Ji part: "Acharya Manish Ji" (cream text, soft shadow).
- Audio: loudnorm the Acharya Ji part to -16 LUFS so it matches the endplate.
- Encode H.264 crf 20 preset veryfast, yuv420p, AAC 192k 48 kHz, +faststart.

## 3. Report
ads/vopd/full/index.md: file, source video id + timestamps, transcript of the Acharya Ji part (Hindi), duration, compliance check line.
Contact sheet per output (8 frames): ads/vopd/full/sheet_<name>.jpg.
Do not post or queue anything. git add ads/vopd only, commit, push. Print one line at the end: FULL ADS READY.
