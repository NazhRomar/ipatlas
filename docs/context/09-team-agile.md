# 09 — Team, Scrum & Workload

## Roster (fill in)

| Member | Scrum role | Technical role | Owns |
|---|---|---|---|
| Nazh | `[Lead Developer / Scrum role?]` | Repo owner, backend, MVP | repo setup, `app/` backend, dashboard |
| `[Name]` | `[Scrum Leader?]` | `[…]` | `[…]` |
| `[Name]` | `[Recorder?]` | `[…]` | `[…]` |
| `[Name]` | `[…]` | `[…]` | see workload split below |

The rubric needs a named **Scrum Leader** and **Recorder** and every member talking about a real contribution. Don't have Nazh be all roles — the Leader/Recorder roles are cheap for teammates and are good evidence for the report.

## Workload split (so one person doesn't carry everything)

Nazh keeps what is hard to hand off (architecture, API clients, routes, dashboard). Hand teammates well-bounded, low-coupling work that still produces *visible repo evidence*:

| Task | Good owner | Why it's safe to delegate |
|---|---|---|
| `tests/` for validators & storage (spec = test matrix in 06) | Teammate B | Self-contained, clear spec, shows up as commits/PRs |
| `.github/workflows/ci.yml`, `Jenkinsfile`, branch protection | Teammate C (small, concrete, demoable) | Boxed task; they can explain the CI trigger on video |
| README.md, screenshots, evidence folder | Teammate C/D | Needs only the running app |
| Report sections 1, 2, 3 (objectives, scope, literature) | Teammates | Pre-drafted in 07 — they edit and cite |
| Report section 4 (Agile part), conclusion | Scrum Leader / Recorder | They hold the meeting records |
| Video editing, scripts, rehearsal | Scrum Leader | Coordination role |
| Manual QA pass using the acceptance checklist in 05 | Any | Creates issues → PRs |

Everyone needs a real, traceable contribution: assign each task as a GitHub issue with an owner and date. The video requires each person to explain their own work, so don't claim work you didn't do.

## Scrum setup

- **Sprint length:** 1 week (or whatever fits the deadline — confirm date, open question #1). Suggested 3 sprints:
  - **Sprint 1 — Foundation:** repo, README skeleton, backend core, validators, ipify/ipapi clients, first tests, CI green.
  - **Sprint 2 — MVP:** routes, storage/cache, dashboard + map, error states, more tests, Jenkinsfile.
  - **Sprint 3 — Polish & deliver:** UI polish, README, report, evidence, video, stretch if time.
- **Ceremonies (lightweight):** sprint planning (30 min), 2–3 short stand-ups/week (15 min, can be chat-based: "done / next / blocked"), sprint review (demo), retro (what to change). Record each in a shared `meeting-notes` doc or GitHub Discussions — the Recorder owns it.
- **Board:** GitHub Projects columns *Backlog · Sprint · In progress · In review · Done*. One issue per user story/task, labeled `backend`, `frontend`, `ci`, `docs`, `video`, `stretch`.
- **Definition of Done:** code merged via PR, reviewed, CI green, tests added, docs updated, demoable.
- **Communication:** `[channel]`; decisions that matter get copied into `CONTEXT.md`.

## Initial product backlog (issue titles — copy/paste)

1. `chore: initialize repo, .gitignore, README skeleton, LICENSE`
2. `feat: IP validator (v4/v6, private/reserved)`
3. `feat: ipify client (public IPv4/IPv6)`
4. `feat: ipapi.co client + response normalizer`
5. `feat: SQLite storage for history + cache`
6. `feat: REST endpoints /api/health, /api/myip, /api/lookup/*, /api/history`
7. `feat: dashboard layout (cards, lookup form)`
8. `feat: Leaflet map + location details`
9. `feat: history table + clear`
10. `feat: error banners and empty states`
11. `test: validators, clients, storage, routes (T01–T20)`
12. `ci: GitHub Actions workflow + README badge`
13. `ci: Jenkinsfile + webhook`
14. `docs: README (setup, run, test, screenshots, API)`
15. `docs: report sections 1–5 + references`
16. `docs: video script, rehearsal, recording`
17. `stretch: compare IPv4 vs IPv6 · CSV export · Webex notification · dark mode toggle`

## Evidence to capture continuously (for report §4 and video §2)

- [ ] Board screenshots at the start and end of each sprint
- [ ] Sprint planning/retro notes (Recorder)
- [ ] PR list with reviews and review comments
- [ ] One real merge conflict + resolution
- [ ] Contributors graph / commit history per member
- [ ] Actions runs: one failing, one fixed
- [ ] Coverage report
- [ ] Meeting cadence proof (chat screenshots)
