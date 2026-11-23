# aks001 ASR A/B: Groq whisper-large-v3 vs Google Chirp 3 (window 5–43 s)

Reference for meaning: YouTube English transcript of LmpEEPMpNLI (179–229 s).
Groq = raw chunked output (before the hand-written spelling-fix table). Chirp = chirp_3, hi-IN, region `us`.

| Engine | Wrong / misspelled words | Dropped phrases |
|---|---|---|
| Groq whisper-large-v3 | **33** | 3 (पता नहीं · ये दूध के साथ फल का · नारियल का दूध ले लो फिर फल खा लो) |
| Chirp 3 | **0** | 0 |

Groq hallucinates at 26.2–31.4 s ("आयुरिवेशप में मनाया" ×3, "मस्ता्यक जितम टेंब्सी").
Chirp's word timings run continuously through that span, so nothing was missed there.

Render: `clips/aks001.mp4` (Chirp transcript, `ass` filter, `shaping=complex`, Noto Sans Devanagari).
Frames: `aks001_chirp_*.jpg` (5.6 वर्णित, 22.7 चाहिए, 30.3 दिक्कत, 36.5 विरुद्ध).
