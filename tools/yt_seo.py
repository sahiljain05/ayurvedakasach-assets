#!/usr/bin/env python3
"""YouTube SEO helpers (sources/YT_SEO.md). YouTube-only metadata: IG/FB captions are never touched.

seo dict (stored per clip in queue.json as "yt_seo"):
  primary, primary_hinglish, secondary[3-5], title, lead, points[3-5], hashtags[3], playlist (key of PLAYLISTS),
  en_title, en_description, comment, source_url
Everything that ends up on YouTube passes post_ig.caption_problems() plus the extra SEO bans below."""
import json, os, re, subprocess, sys, unicodedata, urllib.parse, urllib.request
sys.path.insert(0, "/opt/aks/app")
import post_ig as P

A = "/opt/aks"
KW_CACHE = f"{A}/work/yt_kw_cache.json"
PLAYLIST_CACHE = f"{A}/work/yt_playlists.json"
SEO_LOG = f"{A}/logs/yt_seo.log"
PROMPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yt_seo_prompt.md")
API = "https://www.googleapis.com/youtube/v3"
UPLOAD_API = "https://www.googleapis.com/upload/youtube/v3"
FORCE_SSL = "https://www.googleapis.com/auth/youtube.force-ssl"

# YT_SEO.md 6: topic playlists (key -> title, description)
PLAYLISTS = {
    "diet": ("आहार और खान-पान | Ayurveda Diet",
             "आयुर्वेद के अनुसार क्या खाएं, कब खाएं और किस चीज़ के साथ क्या न खाएं: आचार्य मनीष जी की छोटी-छोटी बातें। "
             "Ayurveda diet tips in Hindi: food combinations, breakfast, fruits, milk and everyday eating habits."),
    "routine": ("दिनचर्या | Daily Routine",
                "आयुर्वेदिक दिनचर्या: सुबह उठने, नहाने, नाश्ते और रात के खाने का सही समय, आचार्य मनीष जी से। "
                "Ayurvedic daily routine (dinacharya) tips in Hindi."),
    "digestion": ("पाचन और पेट | Digestion Tips",
                  "पाचन अच्छा रखने के आयुर्वेदिक नियम: कैसे खाएं, कितना चबाएं, किस हाल में हल्का खाएं। "
                  "Ayurveda digestion tips in Hindi by Acharya Manish Ji."),
    "water": ("पानी और पेय | Water & Drinks",
              "पानी कब, कैसे और कितना पिएं: खाने के साथ पानी, गुनगुना पानी और पेय पर आयुर्वेद की बातें। "
              "Ayurveda tips on drinking water and drinks, in Hindi."),
    "general": ("आयुर्वेद की बातें | Acharya Manish Ji",
                "आचार्य मनीष जी के छोटे वीडियो: रोज़ की ज़िंदगी के लिए आयुर्वेद की आसान बातें। "
                "Short Ayurveda tips in Hindi from Acharya Manish Ji."),
}

# YT_SEO.md 1: never disease names, cure/ilaj/jad se khatm/guaranteed/100% (on top of P.BANNED / NEGATIVE)
SEO_BANNED = [r"\bilaa?j\b", r"इलाज", r"jad se", r"जड़ से", r"guarantee", r"गारंटी", r"100\s*%", r"\bcure", r"ठीक हो जा",
              r"diabet", r"डायबिटीज", r"शुगर की बीमारी", r"cancer", r"कैंसर", r"thyroid", r"थायरॉइड", r"\bB\.?P\b",
              r"blood pressure", r"ब्लड प्रेशर", r"arthrit", r"गठिया", r"\bPCO[DS]\b", r"asthma", r"अस्थमा", r"दमा",
              r"cholesterol", r"कोलेस्ट्रॉल", r"heart attack", r"हार्ट अटैक", r"migraine", r"माइग्रेन", r"piles", r"बवासीर",
              r"kidney stone", r"पथरी", r"fatty liver", r"psoriasis", r"सोरायसिस", r"depression", r"डिप्रेशन", r"obesity",
              r"मोटापा", r"\bIBS\b", r"ulcer", r"अल्सर"]

EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")
SHORTS = "#Shorts"


# ---- keyword validation (YouTube autocomplete, free, no quota) ----
def _load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def suggest(phrase):
    """Autocomplete suggestions for phrase (hl=hi, gl=IN), cached in work/yt_kw_cache.json. None if unreachable."""
    cache = _load(KW_CACHE, {})
    if phrase in cache:
        return cache[phrase]
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=hi&gl=IN&q="
           + urllib.parse.quote(phrase))
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=10))
        cache[phrase] = r[1]
        json.dump(cache, open(KW_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return r[1]
    except Exception:
        return None


# ---- transcript / captions ----
def _ts(sec, sep=","):
    ms = int(round(sec * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def _ass_time(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def timed_lines(c):
    """[(start, end, text)] in clip time. Prefer the clip's rendered .ass (corrected, clip-timed burned captions),
    else the source transcript json (Chirp first) cut to [start, end]."""
    ass = f"{A}/work/{c['id']}.ass"
    if os.path.exists(ass):
        out = []
        for line in open(ass, encoding="utf-8"):
            if line.startswith("Dialogue:"):
                f = line.rstrip("\n").split(",", 9)
                if len(f) == 10 and f[3] == "Cap":
                    txt = re.sub(r"\{[^}]*\}", "", f[9]).replace("\\N", " ").strip()
                    if txt:
                        out.append((_ass_time(f[1]), _ass_time(f[2]), txt))
        if out:
            return out
    src = os.path.splitext(c.get("source", ""))[0]
    for name in [c.get("transcript"), f"{src}.chirp.json", f"{src}.json"]:
        if name and os.path.exists(f"{A}/work/{name}"):
            segs = json.load(open(f"{A}/work/{name}", encoding="utf-8")).get("segments", [])
            s0, s1 = float(c.get("start", 0)), float(c.get("end", 1e9))
            return [(max(0, s["s"] - s0), min(s1, s["e"]) - s0, s["text"].strip())
                    for s in segs if s["e"] > s0 and s["s"] < s1 and s["text"].strip()]
    return []


def transcript_text(c):
    return " ".join(t for _, _, t in timed_lines(c))


def srt(c, max_chars=42):
    """Merge short caption chunks into non-overlapping SRT cues of up to ~max_chars."""
    cues, cur = [], None
    for s, e, t in timed_lines(c):
        if cur and len(cur[2]) + 1 + len(t) <= max_chars:
            cur = (cur[0], max(cur[1], e), cur[2] + " " + t)
        else:
            if cur:
                cues.append(cur)
            cur = (s, e, t)
    if cur:
        cues.append(cur)
    out = []
    for i, (s, e, t) in enumerate(cues):
        if i + 1 < len(cues):
            e = min(e, cues[i + 1][0])
        e = max(e, s + 0.3)
        out.append(f"{i + 1}\n{_ts(s)} --> {_ts(e)}\n{t}\n")
    return "\n".join(out)


# ---- metadata builders ----
def source_url(c):
    if c.get("yt_seo", {}).get("source_url"):
        return c["yt_seo"]["source_url"]
    m = re.match(r"([A-Za-z0-9_-]{11})(?:_|\.|$)", c.get("source", "") or c["id"])
    return f"https://www.youtube.com/watch?v={m.group(1)}" if m else ""


def credit(c, url):
    """YT_SEO.md 3: link the full source video. Guest-doctor clips (webinar mode) keep naming the doctor."""
    sp = (c.get("speaker") or "").strip()
    who = f"{sp} · Acharya Manish Ji" if sp and "manish" not in sp.lower() else "Acharya Manish Ji"
    return f"🎥 {who} (official channel): {url}" if url else f"🎥 {who} (official YouTube)"


def description(c, seo):
    parts = [seo["lead"].strip(), "", *[p.strip() for p in seo["points"]], "", credit(c, source_url(c) or seo.get("source_url", ""))]
    refs = P.research_lines(c)  # 📚 block only if the clip already has one (CAPTION_FIX.md rules)
    if refs:
        parts += ["", "📚 संदर्भ:", *refs]
    parts += ["", P.DISCLAIMER, "", " ".join(seo["hashtags"][:3] + [SHORTS])]
    return "\n".join(parts)


def _tag_len(t):
    return len(t) + (2 if " " in t else 0)  # YouTube counts quotes around tags with spaces


def tags(seo):
    want = [seo["primary"], seo.get("primary_hinglish", ""), *seo.get("secondary", []),
            "Acharya Manish Ji", "आचार्य मनीष जी", "Ayurveda Ka Sach", "आयुर्वेद"]
    out, seen = [], set()
    for t in want:
        t = re.sub(r"[<>,]", "", (t or "")).strip()
        if t and t.lower() not in seen:
            seen.add(t.lower()); out.append(t)
    while len(out) > 15 or sum(_tag_len(t) for t in out) + len(out) - 1 > 450:
        out.pop(-5)  # drop the last secondary phrase first, keep the 4 brand tags
    return out


def problems(c, seo):
    """Every YT_SEO.md hard rule that can be checked. Empty list = OK to apply."""
    p, title, desc, tg = [], seo["title"], description(c, seo), tags(seo)
    if not 40 <= len(title) <= 70:
        p.append(f"title length {len(title)} not 40-70")
    if not seo["primary"] or seo["primary"].split()[0] not in " ".join(title.split()[:4]):
        p.append("primary phrase not in first 3-4 title words")
    if "#" in title:
        p.append("hashtag in title")
    if len(EMOJI_RE.findall(title)) > 1:
        p.append("more than 1 emoji in title")
    if re.search(r"\b[A-Z]{4,}\b", title):
        p.append("ALL CAPS word in title")
    if not any("ऀ" <= ch <= "ॿ" for ch in title):
        p.append("title not in Devanagari")
    if not 600 <= len(desc) <= 1500:
        p.append(f"description length {len(desc)} not 600-1500")
    hs = re.findall(r"#\S+", desc)
    if len(hs) > 5 or hs[:1] != ["#आयुर्वेद"] or hs[-1] != SHORTS or len(seo["hashtags"]) != 3:
        p.append(f"hashtags {hs}")
    if not 3 <= len(seo["points"]) <= 5 or not 3 <= len(seo.get("secondary", [])) <= 5:
        p.append("need 3-5 points and 3-5 secondary phrases")
    if seo.get("playlist") not in PLAYLISTS:
        p.append(f"unknown playlist {seo.get('playlist')}")
    if "http" in seo.get("comment", "") or "www." in seo.get("comment", ""):
        p.append("link in comment")
    blob = "\n".join([title, desc, " ".join(tg), seo.get("en_title", ""), seo.get("en_description", ""), seo.get("comment", "")])
    p += [f"caption_problems: {x}" for x in P.caption_problems(blob)]
    p += [f"banned: {b}" for b in SEO_BANNED if re.search(b, blob, re.I)]
    return p


# ---- generation for new uploads (claude -p, same CLI the daily pipeline uses) ----
def _claude(prompt):
    r = subprocess.run(["claude", "-p", prompt, "--max-turns", "1", "--output-format", "text"],
                       capture_output=True, text=True, timeout=600, cwd=A)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    return json.loads(m.group(0)) if m else None


def generate(c):
    """Pick keywords from the transcript, validate with autocomplete, write title/description/tags. None on failure."""
    tpl = open(PROMPT, encoding="utf-8").read()
    ctx = json.dumps({"id": c["id"], "title": c.get("title"), "topic": c.get("topic"), "hook": c.get("hook"),
                      "speaker": c.get("speaker") or "Acharya Manish Ji", "caption": P.caption_body(c.get("caption", "")),
                      "transcript": transcript_text(c)}, ensure_ascii=False, indent=1)
    try:
        cand = _claude(tpl.replace("{{STEP}}", "candidates").replace("{{CLIP}}", ctx).replace("{{SUGGESTIONS}}", "{}"))
        phrases = [x for x in (cand or {}).get("candidates", []) if isinstance(x, str)][:8]
        sugg = {ph: suggest(ph) for ph in phrases}
        if all(v is None for v in sugg.values()):
            sugg = {"_note": "autocomplete unreachable: use the transcript phrase"}
        feedback = ""
        for _ in range(2):
            seo = _claude(tpl.replace("{{STEP}}", "final").replace("{{CLIP}}", ctx)
                          .replace("{{SUGGESTIONS}}", json.dumps(sugg, ensure_ascii=False, indent=1)) + feedback)
            if not seo:
                continue
            seo["source_url"] = source_url(c)
            seo["title"] = unicodedata.normalize("NFC", seo.get("title", "")).strip()
            pr = problems(c, seo)
            if not pr:
                return seo
            feedback = "\n\nYour previous answer failed these checks, fix them:\n" + "\n".join(pr) + "\n" + json.dumps(seo, ensure_ascii=False)
    except Exception as ex:
        print("YT SEO generation error", c["id"], ex)
    return None


# ---- YouTube API calls (videos.update / captions / playlists / comments need the youtube.force-ssl scope) ----
def has_force_ssl(tok):
    try:
        info = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/tokeninfo?access_token=" + tok, timeout=30))
        return FORCE_SSL in info.get("scope", "").split()
    except Exception:
        return False


def _req(Y, tok, method, url, body=None, headers=None, data=None):
    h = {"Authorization": f"Bearer {tok}"}
    if body is not None:
        data = json.dumps(body).encode(); h["Content-Type"] = "application/json; charset=UTF-8"
    h.update(headers or {})
    return json.load(Y._open(urllib.request.Request(url, data=data, method=method, headers=h), 120))


def with_long_link(desc, c):
    """YT_LONG.md 4: the next 3 Shorts on a long video's topic carry "पूरा वीडियो: <url>" (after the first paragraph)."""
    url = c.get("yt_long_url")
    if not url or url in desc:
        return desc
    head, sep, rest = desc.partition("\n\n")
    return f"{head}\n\nपूरा वीडियो: {url}" + (f"\n\n{rest}" if sep else "")


def snippet(seo, c):
    return {"title": seo["title"], "description": with_long_link(description(c, seo), c), "tags": tags(seo), "categoryId": "27",
            "defaultLanguage": "hi", "defaultAudioLanguage": "hi"}


def localizations(seo):
    return {"en": {"title": seo["en_title"][:100], "description": seo["en_description"]}}


def videos_update(Y, tok, vid, c, seo):
    body = {"id": vid, "snippet": snippet(seo, c), "localizations": localizations(seo),
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}
    return _req(Y, tok, "PUT", f"{API}/videos?part=snippet,status,localizations", body)


def captions_insert(Y, tok, vid, c):
    text = srt(c)
    if not text.strip():
        raise RuntimeError("no timed transcript for clip")
    b = "aksSEOboundary"
    meta = {"snippet": {"videoId": vid, "language": "hi", "name": "Hindi", "isDraft": False}}
    data = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + text.encode("utf-8") + f"\r\n--{b}--\r\n".encode()
    return _req(Y, tok, "POST", f"{UPLOAD_API}/captions?part=snippet&uploadType=multipart", data=data,
                headers={"Content-Type": f"multipart/related; boundary={b}"})


def captions_list(Y, tok, vid):
    return _req(Y, tok, "GET", f"{API}/captions?part=snippet&videoId={vid}").get("items", [])


def playlists(Y, tok, charge):
    """{key: playlistId}; finds existing playlists by title before creating any (create once)."""
    cache = _load(PLAYLIST_CACHE, {})
    if all(k in cache for k in PLAYLISTS):
        return cache
    have, page = {}, ""
    while True:
        r = _req(Y, tok, "GET", f"{API}/playlists?part=snippet&mine=true&maxResults=50" + (f"&pageToken={page}" if page else ""))
        charge("playlists", "list", 1)
        have.update({i["snippet"]["title"]: i["id"] for i in r.get("items", [])})
        page = r.get("nextPageToken")
        if not page:
            break
    for k, (title, desc) in PLAYLISTS.items():
        if k in cache:
            continue
        if title in have:
            cache[k] = have[title]
        else:
            r = _req(Y, tok, "POST", f"{API}/playlists?part=snippet,status,localizations",
                     {"snippet": {"title": title, "description": desc, "defaultLanguage": "hi"},
                      "status": {"privacyStatus": "public"}})
            charge("playlists", f"created {k} {r['id']}", 50)
            cache[k] = r["id"]
        json.dump(cache, open(PLAYLIST_CACHE, "w"), ensure_ascii=False, indent=1)
    return cache


def playlist_add(Y, tok, pid, vid):
    return _req(Y, tok, "POST", f"{API}/playlistItems?part=snippet",
                {"snippet": {"playlistId": pid, "resourceId": {"kind": "youtube#video", "videoId": vid}}})


def comment(Y, tok, channel, vid, text):
    # The Data API has no endpoint to pin a comment, so it is only posted (YT_SEO.md 7 allows this).
    return _req(Y, tok, "POST", f"{API}/commentThreads?part=snippet",
                {"snippet": {"channelId": channel, "videoId": vid,
                             "topLevelComment": {"snippet": {"textOriginal": text}}}})


def log(c, seo, steps):
    from datetime import datetime, timezone
    rec = {"t": datetime.now(timezone.utc).isoformat(), "id": c["id"], "video": c.get("yt_video_id"),
           "title": seo["title"], "description": description(c, seo), "tags": tags(seo),
           "playlist": PLAYLISTS[seo["playlist"]][0], "steps": steps}
    with open(SEO_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
