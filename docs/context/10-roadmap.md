# 10 — Roadmap & Live Task Checklist

Order optimizes for: **something demoable early**, then tests/CI, then polish. Tick items as done; mirror them as GitHub issues.

## Phase 0 — Repo & scaffolding (≈ 1–2 h)

- [ ] Create **public** GitHub repo (name e.g. `ipatlas`); add teammates as collaborators
- [ ] Local: `git init`, connect remote, first commit (docs + CONTEXT)
- [ ] `.gitignore`, `requirements.txt`, `requirements-dev.txt`, `.env.example`, LICENSE (MIT)
- [ ] Branches: `main`, `develop`; enable branch protection on `main` (PR + status check)
- [ ] GitHub Projects board + issues from `09-team-agile.md` backlog
- [ ] PR template (`.github/pull_request_template.md`)
- [ ] Python env (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
```

## Phase 1 — Backend core (Nazh)

- [ ] `app/` factory + config + `run.py`; `GET /api/health`
- [ ] `validators.py` (+ tests T01–T04)
- [ ] `ipify_client.py` (+ T05–T07)
- [ ] `ipapi_client.py` + normalize (+ T08–T12) — **check live ipapi.co response/fields once with curl and save a sample JSON under `tests/fixtures/`**
- [ ] `errors.py` + handlers
- [ ] `storage.py` (+ T13–T15)
- [ ] Routes `/api/myip`, `/api/lookup/me`, `/api/lookup/<ip>`, `/api/history` (+ T16–T20)

## Phase 2 — CI (can run in parallel with Phase 3 — hand to teammate)

- [ ] `.github/workflows/ci.yml`, first green run, README badge
- [ ] `Jenkinsfile` (+ Jenkins instance + webhook if feasible)
- [ ] Coverage threshold 80%

## Phase 3 — MVP dashboard (Nazh)

- [ ] Layout + styles (05)
- [ ] Fetch helper, `render()`, IPv4/IPv6 cards
- [ ] Lookup form + presets
- [ ] Leaflet map pin + popup
- [ ] History table + clear
- [ ] Error banners, loading and empty states
- [ ] Manual acceptance checklist (05)

## Phase 4 — Polish & stretch (only if Phases 1–3 done)

- [ ] Compare IPv4 vs IPv6 view
- [ ] CSV/JSON export
- [ ] Webex notification (REST `POST /v1/messages` with a bot token in `.env`)
- [ ] Dark mode toggle

## Phase 5 — Documentation

- [ ] README finished (what/why, screenshots, setup, run, test, API table, CI badge, team)
- [ ] Architecture diagram exported as PNG
- [ ] Evidence screenshots collected
- [ ] Report written per `07-report-outline.md`; ≥15 references verified
- [ ] Export PDF: title page, 12pt, single spaced → check page layout

## Phase 6 — Video

- [ ] Script per `08-video-pitch.md`; each member's part written
- [ ] Rehearse demo twice; record; upload (unlisted) or export MP4
- [ ] Repo link in description

## Final submission checklist

- [ ] PDF named per instructor convention
- [ ] Repo public, README renders, CI green on `main`
- [ ] Video link accessible without login
- [ ] Repo link in PDF and video description
- [ ] Everyone's contribution visible in git history

## Suggested immediate next step

Phase 0, then tell Claude: *"Scaffold the Flask app and implement Phase 1 starting with validators and tests"* — Claude can generate the code in this folder, run `pytest`, and iterate.
