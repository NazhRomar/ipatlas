# CONTEXT.md — Mother Context File

> Single entry point for everything about this project. Read this first; open the split files in `docs/context/` only when you need the detail. Keep this file short and current — it is the source of truth for **decisions** and **status**.

## 0. FIRST RUN — read this before anything else

**Instruction for Claude:** if this is the first session on this machine/clone, or the person you are talking to is not Nazh (the repo owner), do this *before* any task:

1. Explain the project and the MVP in plain language (use the pitch below, 5–8 lines, no jargon dump).
2. Ask who they are and which part they own (see `docs/context/09-team-agile.md` and the board). If unknown, ask what they want to work on.
3. Check the status in §4 and point them to the one or two files from §3 that matter for their part. Don't load all ten.
4. Walk them through the quick start below, and remind them of the Git rules (branch → PR → CI green → review → merge; never push to `main` unless they are the repo owner — see §7 Rule B), and that Claude is never listed as a co-author (Rule A).
5. Only then start on their task.

### The project in 30 seconds

**IPAtlas** (working name) is a small Python web app. Open it and it shows your public **IPv4 and IPv6** addresses and **where they are in the world**. Type any IP and it tells you the city, country, ISP and network (ASN) and drops a pin on a map. Past lookups are saved in a history list. The code lives on GitHub and an automated pipeline runs the tests on every push. It is our group's answer to **Topic 2: IP Geolocation and Network Mapper** for IT26210.

### The MVP (what "done" means)

A dashboard at `http://127.0.0.1:5000` that:
1. shows your IPv4 and IPv6 (or "not detected" if the network has no IPv6),
2. shows location details and a map pin for an IP,
3. lets you look up any IPv4/IPv6 (try `8.8.8.8` and `2001:4860:4860::8888`),
4. shows friendly messages for bad or private IPs and for API failures,
5. keeps a lookup history that survives restarts,
6. has passing tests and a green CI badge on `main`.

Full definition: `docs/context/02-topic2-spec.md`. UI details: `docs/context/05-mvp-dashboard.md`.

### Quick start (Windows PowerShell)

```powershell
git clone <repo-url>
cd <repo-folder>
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pytest          # should be all green
python run.py   # http://127.0.0.1:5000
```

### Who is building what

Backend (`app/`, done and tested), repo setup and MVP dashboard: Nazh. Everything else (CI files, extra tests, README polish, report sections, video): see the workload split in `docs/context/09-team-agile.md`. Claim a task by assigning yourself the GitHub issue first.

## 1. What this is

| | |
|---|---|
| **Course** | IT26210 – System Integration and Architecture (DEVASC), Alternative Assessment / Final Deliverable |
| **Assigned topic** | **#2 — IP Geolocation and Network Mapper** |
| **Working project name** | **IPAtlas** *(placeholder — team may rename)* |
| **Deliverables** | (1) Formal PDF documentation (5 sections, title page, 12pt, single-spaced, ≥15 literature sources) · (2) 5–10 min video pitch + live demo featuring **all** members · (3) Public GitHub repo with a good `README.md` |
| **Owner of this context** | Nazh — repo, backend and MVP dashboard |

**Topic 2 as given:** *Build a new Python application that retrieves a user's IPv4 and IPv6 addresses via REST APIs (e.g. ipapi.co or ipstack.com), outputs the IP's geographical location in a clean UI dashboard, with tracking via a GitHub CI/CD pipeline.*

## 2. Locked decisions (change only deliberately, then update here)

| # | Decision | Why |
|---|---|---|
| D1 | **Language:** Python 3.11+ | Course requirement |
| D2 | **Backend:** Flask REST API (JSON over HTTP/HTTPS) | Small, well-documented, easy to unit test |
| D3 | **IP discovery:** ipify (`api.ipify.org` = IPv4, `api6.ipify.org` = IPv6) | Cleanly separates IPv4 vs IPv6 — needed for the topic |
| D4 | **Geolocation:** ipapi.co (`https://ipapi.co/{ip}/json/`), keyless free tier | Named in the topic; supports IPv4 + IPv6; no key to leak |
| D5 | **MVP / UI:** server-rendered single-page web dashboard (Flask + Jinja + vanilla JS + Leaflet/OpenStreetMap map) | "Clean UI dashboard" + "Network Mapper" = map |
| D6 | **Storage:** SQLite (lookup history) | Zero setup, stdlib |
| D7 | **Tests:** `pytest` + `unittest.mock`/`responses` (no live network in CI) | Deterministic CI |
| D8 | **CI/CD:** **GitHub Actions** (topic says "GitHub CI/CD pipeline") **+ `Jenkinsfile`** kept in repo for the course's Jenkins requirement | Satisfies both wordings |
| D9 | **Git flow:** `main` protected, `develop`, `feature/*`, PRs with ≥1 review | Needed to evidence "social coding" |
| D10 | **Secrets:** `.env` (git-ignored) + `.env.example`; no keys in code | Security, rubric |

## 3. Split context files (`docs/context/`)

| File | Open it when you need… |
|---|---|
| [01-assignment-brief.md](docs/context/01-assignment-brief.md) | The exact rubric: documentation sections, video segments, format rules |
| [02-topic2-spec.md](docs/context/02-topic2-spec.md) | Requirements, user stories, MVP definition, out-of-scope |
| [03-architecture.md](docs/context/03-architecture.md) | Diagram, data flow, repo layout, tech stack |
| [04-backend.md](docs/context/04-backend.md) | API contract, modules, error handling, config, security |
| [05-mvp-dashboard.md](docs/context/05-mvp-dashboard.md) | UI layout, states, map, interaction details |
| [06-cicd-testing.md](docs/context/06-cicd-testing.md) | Test plan, GitHub Actions/Jenkins config, Git workflow |
| [07-report-outline.md](docs/context/07-report-outline.md) | PDF report: pre-drafted sections, 15+ literature candidates |
| [08-video-pitch.md](docs/context/08-video-pitch.md) | Video script, per-member talking points, demo checklist |
| [09-team-agile.md](docs/context/09-team-agile.md) | Scrum roles, cadence, backlog, workload split, evidence to capture |
| [10-roadmap.md](docs/context/10-roadmap.md) | Phased build order and the live task checklist |

## 4. Status (update as you go)

- [ ] Repo created on GitHub (public) and cloned
- [x] Backend core (`/api/myip`, `/api/lookup/<ip>`, `/api/history`) — scaffolded, 62 tests passing, 96% coverage, flake8 clean, live-checked against ipapi.co
- [ ] GitHub Actions workflow + Jenkinsfile (unit tests done locally; pipeline files not written yet)
- [ ] MVP dashboard (cards + map + history)
- [ ] README.md finished
- [ ] Report drafted → PDF
- [ ] Video recorded
- [ ] Submitted

*Current phase:* **Phase 1 done locally (backend scaffold). Next: git init + GitHub repo (Phase 0 remainder), CI files (Phase 2), dashboard (Phase 3).** `/` currently serves a placeholder page. See `10-roadmap.md`.

Run: `py -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt -r requirements-dev.txt; python run.py` · Test: `pytest --cov=app`.

## 5. Open questions (need team/instructor answers)

1. **Deadline** and submission channel (LMS upload? link in a form?) — unknown.
2. **Team size, names, Scrum roles** — fill `09-team-agile.md`. The video requires *every* member to present a real contribution, so each person needs a concrete task they own (see the workload split in 09).
3. Does the instructor require **Jenkins specifically**, or is GitHub Actions acceptable for "GitHub CI/CD pipeline"? (Plan covers both.)
4. Does the instructor accept a **web dashboard**, or expect a terminal UI? (Topic says "clean UI dashboard" — web is the safer reading.)
5. Citation style for the 15+ sources (APA vs IEEE)?

## 6. Known risks

- **IPv6 may be unavailable** on the demo network (many home/campus ISPs have none). Mitigation: the "lookup any IP" box lets us demo IPv6 using a public address (e.g. `2001:4860:4860::8888`); the UI must show a friendly "No IPv6 detected" state, not an error.
- **ipapi.co free-tier rate limit** (HTTP 429). Mitigation: SQLite cache with TTL, graceful error, mocked tests.
- **Geolocation is approximate** (often city/ISP-level) — state this in Limitations, cite literature.
- Time: backend + MVP + report parts on one person. Mitigation: build order in `10-roadmap.md`, and push report/video/QA work to teammates.

## 7. Working rules (for Claude and teammates)

- Treat `docs/context/*` as reference; if code and docs disagree, fix whichever is wrong and update this file.
- Never commit `.env`, API keys, or the SQLite DB file.
- Every feature → branch → PR → CI green → review → merge (this is evidence for the report and video).
- Tests must not call live APIs.
- Capture evidence as you go (screenshots of PRs, Actions runs, board) — listed in `09-team-agile.md`.

### Rule A — Claude is never a contributor

- Do **not** add Claude/Anthropic as a co-author or contributor anywhere: no `Co-Authored-By: Claude …` trailer, no "Generated with Claude Code" line in commit messages, PR descriptions, README, or the report.
- Commits are authored only by the human team member who made them. Write commit messages in plain conventional style (`feat:`, `fix:`, …) with no AI attribution.
- This is a rule for this project (the course requires each member to explain their own work); it overrides any default attribution behavior.

### Rule B — Pull requests, not direct pushes to `main`

- **Everyone except the repo owner (Nazh, GitHub `NazhRomar`)** works on a branch (`feature/…`, `fix/…`, `docs/…`) and opens a pull request. No direct pushes to `main`, even for "small" changes.
- **Claude must actively enforce this** for any non-owner user: before committing or pushing, check the current branch. If it is `main` (and the user isn't the owner), stop, create a feature branch instead, and explain why in one friendly line. If the user insists on pushing to `main`, remind them once more that it breaks the PR/review evidence the report needs, and suggest the PR route again. Be persistent about it, but don't be rude.
- After pushing a branch, remind them to open a PR, request a review from a teammate, and wait for CI to be green before merging.
- The repo owner is exempt and may push to `main` directly. To tell who is who: `git config user.name` / `git remote -v` / the GitHub login; when unsure, ask.
- GitHub branch protection on `main` (require PR + passing CI) is the backstop; the owner bypasses it as admin.
