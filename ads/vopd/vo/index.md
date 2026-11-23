# VOPD endplate voice-overs

Google Cloud TTS hi-IN Chirp 3 HD (generic synthetic voices, not a clone of any person). LINEAR16 48 kHz WAV, SSML 300 ms breaks at sentence ends. Text exactly as in ENDPLATE_VO.md (TTS input uses "जीना सीखो हिम्स" as written there). Verified by Chirp 3 hi-IN transcription back: every script word present (verify.json).

| file | voice | duration | speakingRate |
|---|---|---|---|
| L1_F.wav | hi-IN-Chirp3-HD-Pulcherrima (female) | 22.26 s | 1.0 | |
| L1_M.wav | hi-IN-Chirp3-HD-Alnilam (male) | 20.58 s | 1.0 | |
| L2_F.wav | hi-IN-Chirp3-HD-Pulcherrima (female) | 20.62 s | 1.0 | |
| L2_M.wav | hi-IN-Chirp3-HD-Alnilam (male) | 19.31 s | 0.95 | ⚠️ OUT OF SPEC: 19.31 s is below the 20 s minimum; this voice speaks the L2 text in 16.8-19.3 s across speakingRate 0.95-1.08. Kept the closest complete take (no silence padding, no rate outside 0.95-1.08). Needs a decision: accept, allow rate < 0.95, or change voice/text. |
