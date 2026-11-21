# 08 — Video Pitch Plan (5–10 min, target ~8:00)

Everyone speaks. Record in one shared call (Meet/Zoom/Discord screen-record) or stitch individual clips. MP4 or unlisted YouTube/Vimeo; put the **GitHub link in the description**.

## Run of show

| Time | Segment | Speaker | Content |
|---|---|---|---|
| 0:00–1:00 | **Intro & roles** | Scrum Leader | Project name IPAtlas; value proposition ("one dashboard to find where any IPv4/IPv6 lives, tested automatically on every commit"); each member says name + role |
| 1:00–2:15 | **How it was made** | Scrum Leader / Recorder | Sprint length, meeting cadence, communication channel; screen-share GitHub Projects board + commit/PR history (proof of delegation) |
| 2:15–5:00 | **Implementation breakdown** | each member ~45–60 s | Member A: backend/API clients + validation (Nazh) · Member B: dashboard/MVP UI (Nazh or teammate) · Member C: tests + CI/CD (teammate) · Member D: docs/README/QA (teammate). Each says *what they built, one design choice, one thing learned* |
| 5:00–5:45 | **Obstacle & fix** | whoever owns it | One bug: e.g. "IPv6 lookup crashed on networks without IPv6 → made ipify v6 return `None`, UI shows 'not detected'" · or team issue: uneven workload → re-sliced tasks |
| 5:45–8:00 | **Live demo** | Nazh (driver) + narrator | See checklist below |
| 8:00–8:30 | **Wrap-up** | All / Leader | What we'd do next; thanks |

## Live demo checklist (rehearse twice)

1. Terminal: `git clone`, create venv, `pip install`, `flask run` — or just show it running (don't spend 2 min on install).
2. Browser: dashboard loads → **my IPv4 / IPv6** + location + map pin.
3. Lookup `8.8.8.8` → pin moves. Lookup `2001:4860:4860::8888` → IPv6 works.
4. Lookup `999.1.1.1` → friendly error. Lookup `192.168.1.1` → "private address" message.
5. Show history table, reload page → persisted.
6. **CI proof:** make a tiny commit on a feature branch → push → open PR → show Actions run going green (have a pre-recorded fallback clip in case Actions is slow). Optionally show the Jenkins build.
7. **Code glimpse (≤ 20 s):** `ipapi_client.normalize()` or the error-mapping block — explain one thing (e.g., API errors arrive inside a 200 JSON body).
8. Show a failing-test run → fix → green (optional, strong evidence of CI value).

## Pre-recording checklist

- [ ] Browser zoom 125%, notifications off, personal tabs/bookmarks hidden, **no email/keys visible**
- [ ] `.env` not on screen
- [ ] Network works (test API quota not exhausted — pre-warm cache for demo IPs, but also show one live miss)
- [ ] Recording 1080p, mic test, no echo
- [ ] Each member's script ≤ 1 minute and rehearsed
- [ ] Repo link in description and on a closing slide

## Per-member talking-point template

> "I'm **[name]**, **[role]**. I implemented **[component]**. The key idea is **[one sentence]**. The hardest part was **[problem]** and I solved it by **[solution]**. You can see it in **[file/PR]**."

## Fallbacks

- Live API down → pre-seeded history rows + screenshot of a successful live run.
- No IPv6 → demonstrate via preset IPv6 chip; explicitly say why.
- Actions slow → show a previous run + the trigger.
