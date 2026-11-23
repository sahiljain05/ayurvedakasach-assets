#!/opt/aks/venv/bin/python
"""VOPD endplate voice-overs (ads/vopd/ENDPLATE_VO.md, part 1).
Google Cloud TTS hi-IN Chirp 3 HD, generic synthetic voices (same as the short-ads job: Pulcherrima F, Alnilam M).
Text used exactly; SSML 300 ms breaks only at sentence ends. LINEAR16 48 kHz -> WAV.
Each VO must be 20-32 s; speakingRate 1.0 first, then within 0.95-1.08 if needed.
Verification: Chirp 3 (hi-IN) transcription back; every script word must be present, else regenerate.
Usage: vopd_vo.py  -> ads/vopd/vo/L1_F.wav ... + ads/vopd/vo/index.md + ads/vopd/vo/verify.json"""
import base64, json, pathlib, re, subprocess, sys, tempfile, urllib.request
sys.path.insert(0, "/opt/aks/app")
import transcribe_chirp as C  # read-only reuse of token()/api()/host()/config()

OUT = pathlib.Path("/opt/aks/assets/ads/vopd/vo")
VOICES = {"F": "hi-IN-Chirp3-HD-Pulcherrima", "M": "hi-IN-Chirp3-HD-Alnilam"}
SCRIPTS = {
    "L1": "क्या आप अपनी सेहत के लिए आयुर्वेद और प्राकृतिक तरीकों को अपनाना चाहते हैं? अब जीना सीखो हिम्स की वर्चुअल ओपीडी में, घर बैठे, वीडियो कॉल पर हमारे आयुर्वेद डॉक्टरों से बात कीजिए। डॉक्टर आपकी बात ध्यान से सुनेंगे, आपकी दिनचर्या और खान-पान समझेंगे, और आयुर्वेद के नज़रिए से आपको मार्गदर्शन देंगे। नीचे दिए लिंक पर क्लिक करें और अपनी वीडियो कंसल्टेशन बुक करें।",
    "L2": "अपनी सेहत को लेकर एक दूसरी राय चाहते हैं? जीना सीखो हिम्स की वर्चुअल ओपीडी में, आयुर्वेद डॉक्टर से घर बैठे वीडियो पर विस्तार से बात कीजिए। अपनी रिपोर्ट्स और अब तक का अनुभव साथ रखिए; डॉक्टर आपकी पूरी बात समझकर आयुर्वेद के अनुसार सलाह देंगे। नीचे दिए लिंक से आज ही अपनी वीडियो कंसल्टेशन बुक करें।",
}
RATES = [1.0, 0.95, 1.05, 1.08]
LO, HI = 20.0, 32.0


def ssml(text):
    sents = [s.strip() for s in re.findall(r"[^?।]+[?।]", text)]
    assert "".join(sents).replace(" ", "") == text.replace(" ", ""), "sentence split lost text"
    return "<speak>" + '<break time="300ms"/>'.join(sents) + "</speak>"


def synth(voice, text, rate, out):
    body = {"input": {"ssml": ssml(text)}, "voice": {"languageCode": "hi-IN", "name": voice},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 48000, "speakingRate": rate}}
    r = C.api("POST", "https://texttospeech.googleapis.com/v1/text:synthesize", body)
    out.write_bytes(base64.b64decode(r["audioContent"]))  # LINEAR16 response already has a WAV header
    return C.duration(out)


def norm(w):
    w = re.sub(r"[^ऀ-ॿ\w]", "", w)
    return w.replace("़", "")  # nukta-insensitive (नज़रिए / नजरिए)


def transcribe(wav):
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d) / "a.flac"
        C.flac(wav, f)
        b64 = base64.b64encode(f.read_bytes()).decode()
    for loc in C.REGIONS:
        try:
            r = C.api("POST", C.host(loc) + "/recognizers/_:recognize", {"config": C.config(), "content": b64})
            return " ".join(a["alternatives"][0]["transcript"] for a in r.get("results", []) if a.get("alternatives"))
        except RuntimeError as e:
            last = e
    raise last


def missing_words(script, heard):
    got = {norm(w) for w in heard.split()}
    glued = norm("".join(heard.split()))
    return [w for w in (norm(x) for x in script.split()) if w and w not in got and w not in glued]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, report = [], {}
    for sid, text in SCRIPTS.items():
        for g, voice in VOICES.items():
            out = OUT / f"{sid}_{g}.wav"
            best, near = None, None  # near = complete take closest to the 20-32 s window (if none fits)
            for rate in RATES:
                for take in range(3):
                    dur = synth(voice, text, rate, out)
                    heard = transcribe(out)
                    miss = missing_words(text, heard)
                    print(f"{out.name} rate={rate} take={take} dur={dur:.2f} missing={miss}", flush=True)
                    if not miss:
                        gap = max(LO - dur, dur - HI, 0)
                        if near is None or gap < near[0]:
                            near = (gap, rate, dur, heard, out.read_bytes())
                        if gap == 0:
                            break
                if not miss and LO <= dur <= HI:
                    best = (rate, dur, heard)
                    break
            note = ""
            if not best:
                if not near:
                    sys.exit(f"{out.name}: no take with every word present")
                _, rate, dur, heard, data = near
                out.write_bytes(data)
                note = (f" ⚠️ OUT OF SPEC: {dur:.2f} s is below the 20 s minimum; this voice speaks the L2 text in"
                        f" 17-19.6 s across speakingRate 0.95-1.08. Kept the closest complete take (no silence padding,"
                        f" no rate outside 0.95-1.08). Needs a decision: accept, allow rate < 0.95, or change voice/text.")
                print(f"{out.name}: OUT OF SPEC, kept {dur:.2f}s @ {rate}", flush=True)
            else:
                rate, dur, heard = best
            rows.append(f"| {out.name} | {voice} ({'female' if g == 'F' else 'male'}) | {dur:.2f} s | {rate} |{note} |")
            report[out.name] = {"voice": voice, "rate": rate, "dur": round(dur, 2), "chirp_back": heard, "missing": [],
                                "in_spec": bool(best)}
    (OUT / "verify.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    (OUT / "index.md").write_text(
        "# VOPD endplate voice-overs\n\nGoogle Cloud TTS hi-IN Chirp 3 HD (generic synthetic voices, not a clone of any person). "
        "LINEAR16 48 kHz WAV, SSML 300 ms breaks at sentence ends. Text exactly as in ENDPLATE_VO.md (TTS input uses "
        "\"जीना सीखो हिम्स\" as written there). Verified by Chirp 3 hi-IN transcription back: every script word present "
        "(verify.json).\n\n| file | voice | duration | speakingRate |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
