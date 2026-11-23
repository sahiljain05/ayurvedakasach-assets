#!/opt/aks/venv/bin/python
"""VOPD endplate videos (ads/vopd/ENDPLATE_VO.md, part 2): b-roll + voice-over + compliance footer.
Usage: vopd_broll_mux.py [L1_F L1_M L2_F L2_M]   (default: all four)
- b-roll: ads/vopd/broll/broll_16x9.mp4 (1920x1080, silent, last 4 s = title card)
- VO starts at 0.4 s. If 0.4 + VO + 0.8 > b-roll length: hold the last frame (tpad clone) to VO end + 0.8 s;
  never speed up or cut the VO. Else: pad the audio with silence to the b-roll length.
- Audio: loudnorm -16 LUFS (two-pass), AAC 192k 48 kHz mono.
- Footer for the whole video (libass, shaping=complex, Noto Sans 26 px, #F6EEDC on a 55% dark bar, 24 px from bottom).
- H.264 crf 20 veryfast yuv420p +faststart. Contact sheet with 6 frames per output."""
import json, pathlib, re, subprocess, sys, tempfile

R = pathlib.Path("/opt/aks/assets/ads/vopd")
BROLL, VO, OUT = R / "broll/broll_16x9.mp4", R / "vo", R / "endplate"
FOOTER = ("Consultation and guidance only · Do not stop or change ongoing treatment without your doctor's advice"
          " · Individual experiences vary · AI voice")
START, TAIL = 0.4, 0.8
W, H = 1920, 1080
BOX = 8  # ASS box padding (Outline with BorderStyle 3); bar bottom edge = MarginV - BOX = 24 px
NICE = ["nice", "-n", "15", "ionice", "-c3"]


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def ass_file(path, length):
    # ASS colours are &HAABBGGRR, AA = transparency. Text #F6EEDC opaque; bar black at 55% opacity -> AA = 0x73.
    end = f"{int(length // 3600)}:{int(length % 3600 // 60):02d}:{length % 60:05.2f}"
    path.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Footer,Noto Sans,26,&H00DCEEF6,&H00DCEEF6,&H73000000,&H73000000,0,0,0,0,100,100,0,0,3,{BOX},0,2,20,20,{24 + BOX},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{end},Footer,,0,0,0,,{FOOTER}
""", encoding="utf-8")


def loudnorm_args(vo):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(vo), "-af",
                          "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    return (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def sheet(video, out, length):
    with tempfile.TemporaryDirectory() as d:
        frames = []
        for i in range(6):
            t = length * (i + 0.5) / 6
            f = f"{d}/{i}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                            "-vf", f"scale=640:-2,drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:"
                            f"text='{t:.1f}s':x=8:y=8:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", f], check=True)
            frames.append(f)
        inputs = sum((["-i", f] for f in frames), [])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                        "".join(f"[{i}]" for i in range(6)) + "xstack=inputs=6:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0",
                        "-q:v", "3", str(out)], check=True)


def make(name):
    vo = VO / f"{name}.wav"
    out = OUT / f"vopd_endplate_{name}.mp4"
    bl, vd = dur(BROLL), dur(vo)
    need = START + vd + TAIL
    length = max(bl, need)
    vf = f"tpad=stop_mode=clone:stop_duration={need - bl:.3f}," if need > bl else ""
    with tempfile.TemporaryDirectory() as d:
        ass = pathlib.Path(d) / "footer.ass"
        ass_file(ass, length)
        vf += f"ass={ass}:shaping=complex,format=yuv420p"
        af = (f"{loudnorm_args(vo)},aresample=48000,aformat=channel_layouts=mono,"
              f"adelay={int(START * 1000)}:all=1,apad=whole_dur={length:.3f},atrim=0:{length:.3f}")
        subprocess.run([*NICE, "ffmpeg", "-y", "-loglevel", "error", "-i", str(BROLL), "-i", str(vo),
                        "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1", "-movflags", "+faststart",
                        "-t", f"{length:.3f}", "-threads", "2", str(out)], check=True)
    sheet(out, OUT / f"sheet_{name}.jpg", length)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1]
    info = {"file": out.name, "vo": vo.name, "vo_dur": round(vd, 2), "broll": round(bl, 2),
            "extended": need > bl, "length": round(dur(out), 2), "lufs": float(lufs)}
    print(json.dumps(info), flush=True)
    return info


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[1:] or ["L1_F", "L1_M", "L2_F", "L2_M"]:
        make(n)
