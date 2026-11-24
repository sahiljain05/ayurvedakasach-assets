#!/opt/aks/venv/bin/python
"""YT_LONG.md (user approved 25 Nov 2026): build one 6-12 min landscape YouTube video from a plan.

  long_build.py build <dir>                  render <dir>/plan.json -> <dir>/<LID>_final.mp4 + report.json
  long_build.py approve <dir> --notes "..."  after the semantic compliance review of the final Chirp transcript
  long_build.py meta <dir>                   validate <dir>/meta.json, write description.txt; status -> ready
  long_build.py reject <dir> "reason"        move <dir> to work/long_review/, log the reason (never posted)

<dir> = /opt/aks/work/long/<LID>. plan.json:
{"id": "L2026-11-27", "post_date": "2026-11-27", "format": "compilation" | "single", "topic": "...",
 "title_card": "intro card text", "hook": "1-line text hook", "outro_points": ["...", ...],
 "thumb": {"segment": 0, "t": 12.3, "text": "3-5 big Hindi words"},     # t = seconds in that segment's file
 "segments": [{"video_id": "<11-char YT id>", "file": "<file in /opt/aks/source>", "offset": <file second 0 in the
               original video>, "transcript": "<json in /opt/aks/work, default <file stem>.json>",
               "start": s, "end": e, "cuts": [[a, b], ...], "chapter": "नियम 1: ...", "lower_third": "आचार्य मनीष जी"}]}
Video: intro card 5 s, hook card 3 s, [chapter card 3 s + segment] x N, outro 10 s. 1920x1080 30 fps, fit + blur,
H.264 crf 20, loudnorm -16 LUFS on the joined audio. Burned Hindi captions in the reel style (render.py).
Checks (report.json): segment count/lengths, total 6-12 min, framing QC per segment (qc.check, landscape), Shorts
reuse <= 30 % (clips that went out in the last 30 days), Chirp 3 transcript of the final video screened
(hard: BANNED claims, phone numbers; flags: disease/medicine/hospital/price/BRC words -> must be judged in approve)."""
import hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

A = Path("/opt/aks"); SRC = A / "source"; WORK = A / "work"; REVIEW = WORK / "long_review"
LOG_MD = A / "assets/sources/long_log.md"; PLAN_MD = A / "assets/sources/long_plan.md"
sys.path.insert(0, str(A / "app")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import post_ig as P  # BANNED, DISCLAIMER, caption_problems
import yt_seo as S   # SEO_BANNED, PLAYLISTS, suggest

INTRO, HOOK, CHAP, OUTRO = 5.0, 3.0, 3.0, 10.0
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
FONT = "Noto Sans Devanagari"
HARD = [(b, "banned claim") for b in P.BANNED] + [(r"(?<!\d)\d{10}(?!\d)|\+91|(?<!\d)\d{5}[ -]\d{5}(?!\d)", "phone number")]
FLAG = S.SEO_BANNED + [r"हॉस्पिटल|अस्पताल|hospital", r"बिस्वरूप|biswaroop|\bBRC\b|डीआईपी|\bDIP\b", r"मरीज|patient",
                       r"दवा|दवाई|medicine|गोली", r"बीमारी|रोग", r"रुपये|रुपए|₹|पैकेज|package|फीस|\bfees?\b", r"कैंप|camp"]


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def hms(t):
    t = int(t); return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def srt_ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


def run(cmd):
    subprocess.run(cmd, check=True)


HDR = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},62,&H00FFFFFF,&H0000D7FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,120,120,70,1
Style: Lower,{FONT},44,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB4202020,1,0,0,0,100,100,0,0,3,10,0,1,70,70,190,1
Style: Title,{FONT},92,&H0000D7FF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,4,0,5,140,140,0,1
Style: Sub,{FONT},54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,0,5,160,160,0,1
Style: Small,{FONT},40,&H00C8C8C8,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,80,80,60,1
Style: Point,{FONT},56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,0,7,260,160,0,1
Style: Thumb,{FONT},120,&H0000E6FF,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,0,0,1,9,4,2,50,50,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def esc(t):
    return str(t).replace("\n", "\\N").replace("{", "(").replace("}", ")")


def card(path, d, events):
    """Silent card: dark background + text events [(style, text, start, end, pos or None)]."""
    ass = path.with_suffix(".ass")
    ev = [f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{('{\\pos(%d,%d)}' % pos) if pos else ''}{esc(tx)}" for st, tx, a, b, pos in events]
    ass.write_text(HDR + "\n".join(ev) + "\n", encoding="utf-8")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=0x15110c:s=1920x1080:r=30:d={d}",
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(d),
         "-vf", f"ass={ass}:fontsdir=/usr/share/fonts:shaping=complex", *ENC, str(path)])


def keep_ranges(seg):
    rs, (s, e) = [], (float(seg["start"]), float(seg["end"]))
    cur = s
    for a, b in sorted(seg.get("cuts", [])):
        if b <= cur or a >= e:
            continue
        if a > cur:
            rs.append((cur, a))
        cur = max(cur, b)
    if cur < e:
        rs.append((cur, e))
    return [(a, b) for a, b in rs if b - a > 0.05]


def seg_words(seg, ranges):
    src = SRC / seg["file"]
    tr = json.loads((WORK / seg.get("transcript", src.stem + ".json")).read_text())
    seen, out = set(), []
    for x in tr["segments"]:
        for w in x["words"]:
            if (w["s"], w["e"]) in seen:
                continue
            seen.add((w["s"], w["e"]))
            for k, (a, b) in enumerate(ranges):
                if w["s"] >= a - 0.05 and w["e"] <= b + 0.05:
                    out.append((k, w)); break
    out.sort(key=lambda kw: kw[1]["s"])
    return out


def render_segment(i, seg, d):
    ranges = keep_ranges(seg)
    base = [sum(b - a for a, b in ranges[:k]) for k in range(len(ranges))]
    tmap = lambda k, t: base[k] + max(0.0, t - ranges[k][0])
    total = sum(b - a for a, b in ranges)
    chunks, cur = [], []
    for k, w in seg_words(seg, ranges):
        if cur and cur[-1][0] != k:
            chunks.append(cur); cur = []
        cur.append((k, w))
        if len(cur) >= 4 or w["w"].strip().endswith(("।", "?", "!", ",")):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    cues = []
    for j, c in enumerate(chunks):
        a = tmap(c[0][0], c[0][1]["s"]); b = min(total, tmap(c[-1][0], c[-1][1]["e"]) + 0.15)
        if j + 1 < len(chunks):
            b = min(b, tmap(chunks[j + 1][0][0], chunks[j + 1][0][1]["s"]) - 0.02)
        txt = "".join(w["w"] for _, w in c).strip()
        if txt and b > a:
            cues.append((a, b, txt))
    ev = [f"Dialogue: 0,{ts(0.3)},{ts(min(4.5, total))},Lower,,0,0,0,,{esc(seg.get('lower_third') or 'आचार्य मनीष जी')}"]
    ev += [f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{esc(t)}" for a, b, t in cues]
    ass = d / f"seg{i:02d}.ass"; ass.write_text(HDR + "\n".join(ev) + "\n", encoding="utf-8")
    n = len(ranges)
    fc = "".join(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{k}];[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{k}];"
                 for k, (a, b) in enumerate(ranges))
    fc += "".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac];"
    fc += ("[vc]fps=30,split=2[b1][b2];[b1]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
           "boxblur=24:4,eq=brightness=-0.08[bg];[b2]scale=1920:1080:force_original_aspect_ratio=decrease[fg];"
           f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,ass={ass}:fontsdir=/usr/share/fonts:shaping=complex[v];"
           "[ac]aresample=48000[a]")
    out = d / f"seg{i:02d}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(SRC / seg["file"]), "-filter_complex", fc,
         "-map", "[v]", "-map", "[a]", *ENC, str(out)])
    return out, total, cues, ranges


def reuse_ratio(plan):
    """Seconds of this video that overlap Shorts posted in the last 30 days / content seconds.
    Clips cut from a window file without a known offset count in full against any segment of the same video."""
    q = json.load(open(A / "assets/queue.json"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    segs = [(s["video_id"], [(float(s["offset"]) + a, float(s["offset"]) + b) for a, b in keep_ranges(s)]) for s in plan["segments"]]
    content = sum(b - a for _, rs in segs for a, b in rs)
    used, hits = 0.0, []
    for c in q:
        times = [c.get(k) for k in ("posted_ig_at", "posted_fb_at", "posted_yt_at") if c.get(k)]
        if not times or max(datetime.fromisoformat(t) for t in times) < cutoff:
            continue
        m = re.match(r"([A-Za-z0-9_-]{11})(_w\d+)?\.", c.get("source", ""))
        if not m:
            continue
        off = 0.0 if not m.group(2) else c.get("live_offset")
        cs, ce = float(c["start"]), float(c["end"])
        for vid, rs in segs:
            if vid != m.group(1):
                continue
            ov = (ce - cs) if off is None else sum(max(0.0, min(b, off + ce) - max(a, off + cs)) for a, b in rs)
            if ov > 0:
                used += ov; hits.append(f"{c['id']} {ov:.0f}s"); break
    return (used / content if content else 0.0), hits


def screen(text):
    hard = sorted({f"{why}: {m.group(0)}" for p, why in HARD for m in re.finditer(p, text, re.I)})
    flags = []
    for p in FLAG:
        for m in re.finditer(p, text, re.I):
            flags.append(text[max(0, m.start() - 60):m.end() + 60].replace("\n", " "))
    return hard, flags


def build(d):
    plan = json.loads((d / "plan.json").read_text()); lid = plan["id"]
    rep = {"id": lid, "built_at": datetime.now(timezone.utc).isoformat(), "problems": [], "status": "building"}
    segs, fmt = plan["segments"], plan["format"]
    lens = [sum(b - a for a, b in keep_ranges(s)) for s in segs]
    if fmt == "compilation":
        if not 5 <= len(segs) <= 10:
            rep["problems"].append(f"compilation needs 5-10 segments, has {len(segs)}")
        rep["problems"] += [f"segment {i} length {l:.0f}s not 40-120" for i, l in enumerate(lens) if not 40 <= l <= 120]
        if len({s["video_id"] for s in segs}) < 2:
            rep["problems"].append("compilation segments must come from different sources")
    elif fmt == "single":
        if len(segs) != 1 or not 360 <= lens[0] <= 720:
            rep["problems"].append(f"single format needs one 6-12 min segment, has {len(segs)} / {lens}")
    else:
        rep["problems"].append(f"unknown format {fmt}")
    ratio, hits = reuse_ratio(plan)
    rep["shorts_reuse"] = {"ratio": round(ratio, 3), "clips": hits}
    if ratio > 0.30:
        rep["problems"].append(f"Shorts reuse {ratio:.0%} > 30%")
    parts, chapters, srt, qc_res = [], [], [], []
    card(d / "c_intro.mp4", INTRO, [("Title", plan["title_card"], 0, INTRO, None),
                                    ("Small", "आयुर्वेद का सच · @ayurvedakasach", 0, INTRO, None)])
    card(d / "c_hook.mp4", HOOK, [("Sub", plan["hook"], 0, HOOK, None)])
    parts += [d / "c_intro.mp4", d / "c_hook.mp4"]
    t = INTRO + HOOK
    sys.path.insert(0, str(A / "app")); import qc
    qc.W, qc.H = 960, 540  # landscape sampling for the face QC
    for i, s in enumerate(segs):
        cp = d / f"c_chap{i:02d}.mp4"
        card(cp, CHAP, [("Title", s["chapter"], 0, CHAP, None)])
        chapters.append((0.0 if i == 0 else t, s["chapter"]))
        parts.append(cp); t += dur(cp)
        out, total, cues, ranges = render_segment(i, s, d)
        srt += [(t + a, t + b, tx) for a, b, tx in cues]
        r = qc.check(out, {"start": 0}, f"{lid}_s{i:02d}")
        qc_res.append({"segment": i, "pass": r["pass"], "reason": r["reason"], "sheet": r["sheet"]})
        if not r["pass"]:
            rep["problems"].append(f"segment {i} QC: {r['reason']}")
        parts.append(out); t += dur(out)
    pts = plan["outro_points"][:7]
    ev = [("Title", "सारांश", 0, OUTRO, (960, 110))]
    ev.append(("Point", "\n".join(f"• {p}" for p in pts), 0.3, OUTRO, (260, 210)))
    ev.append(("Small", "पूरी बात सुनें: Acharya Manish Ji official channel", 0, OUTRO, None))
    card(d / "c_outro.mp4", OUTRO, ev)
    chapters.append((t, "सारांश")); parts.append(d / "c_outro.mp4")
    (d / "concat.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    joined = d / "joined.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(d / "concat.txt"), "-c", "copy", str(joined)])
    final = d / f"{lid}_final.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined), "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final)])
    joined.unlink()
    D = dur(final); rep["duration"] = round(D, 1)
    if not 360 <= D <= 720:
        rep["problems"].append(f"final duration {D:.0f}s not 6-12 min")
    ch = [{"t": round(a, 2), "label": hms(a), "title": tt} for a, tt in chapters]
    for k, c in enumerate(ch):
        nxt = ch[k + 1]["t"] if k + 1 < len(ch) else D
        if nxt - c["t"] < 10:
            rep["problems"].append(f"chapter '{c['title']}' shorter than 10 s")
    if len(ch) < 3 or ch[0]["t"] != 0:
        rep["problems"].append("need >= 3 chapters starting at 00:00")
    rep["chapters"] = ch
    (d / "final.srt").write_text("\n".join(f"{k + 1}\n{srt_ts(a)} --> {srt_ts(max(b, a + 0.3))}\n{tx}\n"
                                          for k, (a, b, tx) in enumerate(srt)), encoding="utf-8")
    # thumbnail 1280x720: frame of Acharya Ji + 3-5 big Hindi words
    th = plan["thumb"]; words = th["text"].split()
    if not 3 <= len(words) <= 5:
        rep["problems"].append(f"thumbnail text needs 3-5 words, has {len(words)}")
    tb = [b for b in S.SEO_BANNED + P.BANNED if re.search(b, th["text"], re.I)]
    if tb:
        rep["problems"].append(f"thumbnail text banned words {tb}")
    tass = d / "thumb.ass"
    tass.write_text(HDR.replace("PlayResX: 1920", "PlayResX: 1280").replace("PlayResY: 1080", "PlayResY: 720")
                    + f"Dialogue: 0,{ts(0)},{ts(5)},Thumb,,0,0,0,,{esc(th['text'])}\n", encoding="utf-8")
    ts_src = SRC / segs[th["segment"]]["file"]
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(th["t"]), "-i", str(ts_src), "-frames:v", "1",
         "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1,"
                f"ass={tass}:fontsdir=/usr/share/fonts:shaping=complex", "-q:v", "2", str(d / "thumb.jpg")])
    # Chirp 3 transcript of the final joined video, screened
    subprocess.run([sys.executable, str(A / "app/transcribe_auto.py"), str(final)], check=False)
    tj = WORK / f"{final.stem}.json"
    if not tj.exists():
        rep["problems"].append("final transcript missing")
        text, engine = "", None
    else:
        j = json.loads(tj.read_text()); engine = j.get("engine")
        text = " ".join(s.get("text", "") for s in j.get("segments", []))
    rep["final_transcript"] = {"file": str(tj), "engine": engine, "chars": len(text)}
    if engine and "chirp" not in str(engine).lower():
        rep["problems"].append(f"final transcript engine is {engine}, spec needs Chirp 3")
    hard, flags = screen(text)
    rep["problems"] += [f"transcript {h}" for h in hard]
    rep["flags_to_judge"] = flags
    rep["qc"] = qc_res
    rep["auto_pass"] = not rep["problems"]
    rep["status"] = "built" if rep["auto_pass"] else "failed"
    (d / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    print(json.dumps({k: rep[k] for k in ("id", "status", "duration", "problems", "shorts_reuse")}, ensure_ascii=False))
    print(f"{len(flags)} flagged passages to judge (report.json flags_to_judge); final transcript: {tj}")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def approve(d, notes):
    rep = json.loads((d / "report.json").read_text())
    if not rep.get("auto_pass"):
        sys.exit(f"cannot approve: automatic checks failed {rep['problems']}")
    if rep.get("flags_to_judge") and len(notes) < 20:
        sys.exit("cannot approve: give notes judging every flagged passage")
    rep.update(semantic_check="pass", semantic_notes=notes, sha256=sha(d / f"{rep['id']}_final.mp4"),
               approved_at=datetime.now(timezone.utc).isoformat(), status="approved")
    (d / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1)); print("approved", rep["id"])


def description(plan, rep, meta):
    vids = []
    for s in plan["segments"]:
        if s["video_id"] not in vids:
            vids.append(s["video_id"])
    parts = [*[x.strip() for x in meta["summary"]], "", "अध्याय:", *[f"{c['label']} {c['title']}" for c in rep["chapters"]],
             "", "मुख्य बातें:", *[f"• {p.strip()}" for p in meta["points"]], "",
             "🎥 Acharya Manish Ji (official channel). पूरी बात सुनें, मूल वीडियो:",
             *[f"• https://www.youtube.com/watch?v={v}" for v in vids]]
    refs = [f"• {r['cite']}: {r['note_hi']}" for r in meta.get("research", []) if r.get("cite") and r.get("note_hi")]
    if refs:
        parts += ["", "📚 संदर्भ:", *refs]
    parts += ["", P.DISCLAIMER, "", " ".join(meta["hashtags"])]
    return "\n".join(parts)


def meta(d):
    plan = json.loads((d / "plan.json").read_text()); rep = json.loads((d / "report.json").read_text())
    m = json.loads((d / "meta.json").read_text())
    p = []
    if rep.get("status") != "approved" or rep.get("sha256") != sha(d / f"{rep['id']}_final.mp4"):
        p.append("video not approved (or changed after approval)")
    title = m["title"].strip()
    if not 50 <= len(title) <= 70:
        p.append(f"title length {len(title)} not 50-70")
    if not title.startswith(m["primary"].strip()):
        p.append("title must start with the primary search phrase")
    sug = S.suggest(m["primary"].strip())
    if sug is None:
        p.append("autocomplete unreachable: primary phrase not validated (retry)")
    elif not any(x.strip().lower() == m["primary"].strip().lower() or x.lower().startswith(m["primary"].strip().lower()) for x in sug):
        p.append(f"primary phrase not in YouTube autocomplete: {sug[:5]}")
    if len(m["summary"]) != 2:
        p.append("summary must be 2 lines")
    if len(m["hashtags"]) != 3 or not all(h.startswith("#") for h in m["hashtags"]):
        p.append("need exactly 3 hashtags")
    if m.get("playlist") not in S.PLAYLISTS:
        p.append(f"unknown playlist {m.get('playlist')}")
    if "http" in m.get("comment", "") or not m.get("comment", "").strip().endswith("?"):
        p.append("comment must be a question without links")
    if sum(len(t) + (2 if " " in t else 0) + 1 for t in m["tags"]) > 480:
        p.append("tags too long")
    desc = description(plan, rep, m)
    if len(desc) > 4900:
        p.append(f"description too long {len(desc)}")
    blob = "\n".join([title, desc, " ".join(m["tags"]), m.get("comment", "")])
    p += [f"caption_problems: {x}" for x in P.caption_problems(blob)]
    p += [f"banned: {b}" for b in S.SEO_BANNED if re.search(b, blob, re.I)]
    if p:
        sys.exit("meta problems:\n" + "\n".join(p))
    (d / "description.txt").write_text(desc, encoding="utf-8")
    rep["status"] = "ready"; rep["ready_at"] = datetime.now(timezone.utc).isoformat()
    (d / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    print("ready", rep["id"], "|", title)


def log_md(text):
    if not LOG_MD.exists():
        LOG_MD.write_text("# YouTube long videos log (YT_LONG.md)\n\n", encoding="utf-8")
    with open(LOG_MD, "a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n\n")


def reject(d, reason):
    plan = json.loads((d / "plan.json").read_text()) if (d / "plan.json").exists() else {"id": d.name}
    REVIEW.mkdir(parents=True, exist_ok=True)
    dst = REVIEW / d.name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(d), str(dst))
    log_md(f"## {plan['id']} NOT POSTED ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)\n- topic: {plan.get('topic')}\n"
           f"- format: {plan.get('format')}\n- reason: {reason}\n- moved to: {dst}")
    print("rejected", plan["id"], reason)


if __name__ == "__main__":
    cmd, d = sys.argv[1], Path(sys.argv[2])
    if cmd == "build":
        build(d)
    elif cmd == "approve":
        approve(d, sys.argv[sys.argv.index("--notes") + 1] if "--notes" in sys.argv else "")
    elif cmd == "meta":
        meta(d)
    elif cmd == "reject":
        reject(d, sys.argv[3])
    else:
        sys.exit(__doc__)
