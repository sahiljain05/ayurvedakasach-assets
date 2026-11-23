# Webinar mode (approved by user 23 Nov 2026)

Goal: repurpose long live/webinar recordings on the official @acharyamanishji channel into reels.
Guest doctors: ALL doctors on the channel are allowed (user decision), with name credit. The compliance filter still applies to every clip, unchanged.

## Flow per webinar (one at a time, foreground)
1. Caption-first scan: fetch YouTube captions with vidiq_video_transcript (5 credits). Do NOT import or transcribe the whole video yet.
2. From the captions, shortlist 3-8 windows (25-60 s each) that are:
   - compliance-safe (no cure / reversal / guarantee / stop-medicine / disease-prevention / dosage / sales / phone numbers / camp or hospital promotion),
   - self-contained, start on a sentence boundary, with a strong hook (myth vs fact, surprising everyday tip, clear Q&A),
   - lifestyle topics preferred: food combinations, daily routine, water, sleep, stress, yoga/breathing, seasonal habits, kitchen remedies framed as tradition (not treatment).
   Reject patient testimonials, donation/booking appeals, mantra/havan broadcasts, and any segment showing third-party TV show branding.
3. Import the video via vidIQ. If the import fails for a long video, log it in sources/webinar_log.md and skip it.
4. Cut ONLY the shortlisted windows (+/-10 s padding) and transcribe just those with Chirp 3 (Groq fallback). Never send the full webinar to Chirp.
5. Normal pipeline after that: caption cleanup, research step, render with face/speaker-crop, framing QC, compliance re-check, contact sheet.
6. Speaker credit: identify who is speaking. If it is not Acharya Manish Ji, the caption must name the doctor ("Dr. <name>, Acharya Manish Ji के official channel पर") and the end card line "🎥 Clip: Acharya Manish Ji (official YouTube)" becomes "🎥 Clip: Dr. <name> · Acharya Manish Ji official YouTube". If the speaker cannot be identified with confidence, set needs_review.
7. Spread clips: at most 2 clips from the same webinar per day in the queue order.
8. Delete the full webinar file after its clips are rendered (disk).

## Priority list (start here)
piAh_rqTIjM   # Laughter Chefs 3 live (102k views) - only segments where Acharya Ji speaks and no show branding is visible; if every window shows show branding, skip
6gqkQqlSAFo   # Lucknow live, all diseases: causes and guidance (56 min)
_hZOPMvvQr4   # LIVE on YouTube with Acharya Ji (54 min)
qkxfiVkCPdU   # Special webinar on health and scientific Ayurveda (2h44)
EhqZQRLN3gs   # Building a healthier India through natural healing (1h53)
9zgouWUD-Bk   # Dr Yashika Jain sound healing live (2h28)
9msc0XUtuLY   # Dr Yashika Jain and Dr Sonali Garg live (2h04)
rToI2TFmfbg   # Dr Biswaroop live training (3h02) - extra strict compliance; reject any treatment or cure claim
Rgl6csDRu-s   # Health and wellness guidance live (1h18)
btp7a9t_vs0   # Special online webinar (1h58)
DmWr7zGSa84   # Derabassi camp live (1h13) - reject camp promotion segments
Zi6ajp0wyag   # Meerut live 22 Nov (1h55)
wXNi7FqgUdg   # Meerut live 22 Nov morning (1h45)

## Logging
Append one line per webinar to sources/webinar_log.md: id, windows shortlisted, clips made, rejected reasons, Chirp seconds used.
