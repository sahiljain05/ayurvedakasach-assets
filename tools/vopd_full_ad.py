#!/opt/aks/venv/bin/python
"""VOPD full ads (ads/vopd/FULL_AD.md): Acharya Ji part (16:9) + 0.5 s crossfade into the endplate video.
Usage: vopd_full_ad.py <segment.json> <name> [<name> ...]     e.g. seg_L1.json L1_F L1_M
segment.json: {"src": "<mp4>", "video_id": "...", "src_offset": <seconds of src t=0 in the YouTube video>,
               "start": s, "speech_end": e,                # seconds in src; speech_end = end of the last sentence
               "words": [{"s":..,"e":..,"w":".."}, ...],   # corrected word timings in src seconds
               "credit_margin_v": 40}                      # optional: credit distance from top (px)
- Landscape kept (no crop). Non-16:9 sources: fit on a blurred background.
- Hindi captions on the Acharya Ji part only (reel caption style: Noto Sans Devanagari bold, white, black outline,
  3-4 word chunks, one line at a time), bottom third. Credit "Acharya Manish Ji" top-left (cream, soft shadow).
- Acharya Ji part loudnorm -16 LUFS (two-pass); endplate used as is (already -16 LUFS, has the voice-over).
- The Acharya Ji part runs 0.5 s past speech_end with the audio cut (8 ms fade) at speech_end, so the 0.5 s
  crossfade (xfade + acrossfade) never fades or clips the last spoken word and no next word is heard. H.264 crf 20 veryfast yuv420p, AAC 192k 48 kHz, +faststart.
- 8-frame contact sheet per output. Writes <out>/<file>.json with the facts for index.md."""
import json, pathlib, re, subprocess, sys, tempfile

R = pathlib.Path("/opt/aks/assets/ads/vopd")
OUT = R / "full"
W, H, FPS, XF = 1920, 1080, 60, 0.5
NICE = ["nice", "-n", "15", "ionice", "-c3"]
FF = [*NICE, "ffmpeg", "-y", "-loglevel", "error", "-threads", "2"]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def captions(seg, path):
    start, end = seg["start"], seg["speech_end"]
    d = end - start + XF
    words = sorted((w for w in seg["words"] if w["s"] >= start - 0.05 and w["e"] <= end + 0.05), key=lambda w: w["s"])
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 4 or w["w"].strip().endswith(("।", "?", "!", ",")):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    cy = seg.get("credit_margin_v", 40)  # move below a source logo if one sits top-left
    ev = ["Dialogue: 1,0:00:00.00,%s,Credit,,0,0,%d,,Acharya Manish Ji" % (ts(d), cy)]
    for i, c in enumerate(chunks):
        a, b = max(0, c[0]["s"] - start), min(d, c[-1]["e"] - start + 0.15)
        if i + 1 < len(chunks):
            b = min(b, max(0, chunks[i + 1][0]["s"] - start) - 0.02)
        ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{' '.join(w['w'].strip() for w in c)}")
    # Cap: reel style scaled to 1080p height (78 px @ 1080 wide -> 64 px @ 1080 high); bottom third, above
    # the source's own bottom-edge text strips. Credit: cream #F6EEDC, soft shadow, top-left.
    path.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Noto Sans Devanagari,64,&H00FFFFFF,&H0000D7FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,120,120,170,1
Style: Credit,Noto Sans,34,&H00DCEEF6,&H00DCEEF6,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,0,3,7,48,48,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n", encoding="utf-8")
    return " ".join(w["w"].strip() for w in words)


def loudnorm(src, start, end):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{start}", "-to", f"{end}", "-i", str(src), "-vn", "-af",
                          "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    return (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def part_a(seg, tmp):
    src, start, end = seg["src"], seg["start"], seg["speech_end"]
    vend = end + XF
    ass = tmp / "cap.ass"
    text = captions(seg, ass)
    vw, vh = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                               "stream=width,height", "-of", "csv=p=0", src]).decode().split(","))
    if abs(vw / vh - W / H) < 0.01:
        base = f"[0:v]scale={W}:{H}:flags=lanczos,setsar=1[b]"
    else:  # fit on blurred background
        base = (f"[0:v]split[x][y];[x]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3[bg];"
                f"[y]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[b]")
    vf = f"{base};[b]fps={FPS},ass={ass}:fontsdir=/usr/share/fonts:shaping=complex,format=yuv420p[v]"
    sp = end - start
    af = (f"[0:a]atrim=0:{sp:.3f},{loudnorm(src, start, end)},aresample=48000,aformat=channel_layouts=mono,"
          f"afade=t=out:st={sp - 0.008:.3f}:d=0.008,apad=whole_dur={vend - start:.3f}[a]")
    out = tmp / "a.mp4"
    subprocess.run([*FF, "-ss", f"{start}", "-to", f"{vend}", "-i", src, "-filter_complex", f"{vf};{af}",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "1", str(out)], check=True)
    return out, text


def sheet(video, out, length):
    with tempfile.TemporaryDirectory() as d:
        frames = []
        for i in range(8):
            t = length * (i + 0.5) / 8
            f = f"{d}/{i}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                            "-vf", "scale=640:-2,drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:"
                            f"text='{t:.1f}s':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", f], check=True)
            frames.append(f)
        layout = "|".join(f"{(i % 4) * 640}_{(i // 4) * 360}" for i in range(8))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *sum((["-i", f] for f in frames), []), "-filter_complex",
                        "".join(f"[{i}]" for i in range(8)) + f"xstack=inputs=8:layout={layout}", "-q:v", "3", str(out)],
                       check=True)


def main():
    seg = json.loads(pathlib.Path(sys.argv[1]).read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir="/opt/aks/work") as d:
        a, text = part_a(seg, pathlib.Path(d))
        da = dur(a)
        for name in sys.argv[2:]:
            ep = R / "endplate" / f"vopd_endplate_{name}.mp4"
            out = OUT / f"vopd_full_{name}.mp4"
            fc = (f"[0:v]setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1[v0];"
                  f"[1:v]setpts=PTS-STARTPTS,fps={FPS},format=yuv420p,setsar=1[v1];"
                  f"[v0][v1]xfade=transition=fade:duration={XF}:offset={da - XF:.3f},format=yuv420p[v];"
                  f"[0:a]aresample=48000,aformat=channel_layouts=mono[a0];[1:a]aresample=48000,aformat=channel_layouts=mono[a1];"
                  f"[a0][a1]acrossfade=d={XF}[a]")
            subprocess.run([*FF, "-i", str(a), "-i", str(ep), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                            "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1", "-movflags", "+faststart", str(out)],
                           check=True)
            L = dur(out)
            sheet(out, OUT / f"sheet_{name}.jpg", L)
            meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                                  capture_output=True, text=True).stderr
            info = {"file": out.name, "video_id": seg["video_id"],
                    "yt_start": round(seg["src_offset"] + seg["start"], 2), "yt_end": round(seg["src_offset"] + seg["speech_end"], 2),
                    "acharya_part": round(da, 2), "endplate": ep.name, "total": round(L, 2),
                    "lufs": float(re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1]), "transcript": text,
                    "size_mb": round(out.stat().st_size / 1e6, 1)}
            (OUT / f"{out.stem}.json").write_text(json.dumps(info, ensure_ascii=False, indent=1))
            print(json.dumps(info, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
