# 07 — Formal Documentation (PDF) Outline & Pre-Drafts

Format: title page · PDF · 12pt · single-spaced · numbered headings. Suggested writing tool: Google Docs/Word → export PDF. Keep prose factual; fill `[brackets]` with real data as the project proceeds.

## Title page

Project title · course code/name (IT26210 – System Integration and Architecture) · "Final Deliverable: Alternative Assessment" · team members + roles · section · instructor · date · **GitHub repo URL**.

## 1. Objectives (pre-drafted)

**General Objective:** To develop a Python-based web application that retrieves a user's IPv4 and IPv6 addresses through REST APIs, determines their geographical location, and presents the results on a clean dashboard, with code quality continuously tracked by a GitHub CI/CD pipeline.

**Specific Objectives:**
1. To retrieve public IPv4 and IPv6 addresses and geolocation data over HTTPS using the ipify and ipapi.co REST APIs and parse the JSON responses with Python.
2. To design a Flask-based backend that validates input, normalizes API data, handles upstream errors, and caches lookup history in SQLite.
3. To implement a responsive dashboard that displays IP details and plots the location on an interactive map.
4. To implement Python unit tests (pytest) and a CI/CD pipeline (GitHub Actions, with an equivalent Jenkins pipeline) that automatically tests every commit.
5. To apply Scrum and GitHub social coding (branching, pull requests, code review) throughout development.

## 2. Scope and Limitations (pre-drafted skeleton)

**Scope:** APIs — ipify (address discovery), ipapi.co (geolocation), OpenStreetMap tiles via Leaflet (map). Target — IPv4 and IPv6 public addresses; no network devices are configured. UI — web GUI dashboard (not CLI). Process — Scrum (sprints, backlog, roles), GitHub Projects Kanban, GitHub Flow variant branching. Pipeline — GitHub Actions + Jenkinsfile.

**Limitations:** geolocation is approximate (database-driven, often ISP/city-level — cite Poese et al.); free-tier rate limit of ipapi.co; IPv6 discovery requires an IPv6-capable network; private/reserved addresses can't be geolocated; no authentication or production deployment hardening; no NETCONF/device integration; backlog items not completed: `[list stretch items not done]`.

## 3. Related Literatures — need ≥ 15

Required coverage: (a) network programmability & SDN; (b) APIs integrated; (c) CI/CD, Agile/Scrum. Candidate list below — **verify every detail (authors, year, URL, access date) before citing; choose the style the instructor wants (APA/IEEE).**

| # | Source (candidate) | Use it for |
|---|---|---|
| 1 | Kreutz, D., et al. (2015). *Software-Defined Networking: A Comprehensive Survey.* Proc. IEEE 103(1). | SDN & programmability |
| 2 | Cisco Press — *CCNA DevNet Associate DEVASC 200-901 Official Cert Guide* (Jackson, Gooley, Iliesiu, Malegaonkar, Whaley) | Course foundation: APIs, Git, CI/CD, Agile |
| 3 | Cisco DevNet Associate learning materials (developer.cisco.com/learning) | Network programmability |
| 4 | ipapi.co API documentation (https://ipapi.co/api/) | Geolocation API |
| 5 | ipify API documentation (https://www.ipify.org/) | IPv4/IPv6 discovery |
| 6 | Fielding, R. (2000). *Architectural Styles and the Design of Network-based Software Architectures*, ch. 5 (REST) | REST |
| 7 | RFC 9110 — HTTP Semantics (IETF, 2022) | HTTP status codes/methods |
| 8 | RFC 8259 — The JSON Data Interchange Format (IETF, 2017) | JSON |
| 9 | RFC 791 — Internet Protocol (IPv4) | IPv4 |
| 10 | RFC 8200 — Internet Protocol, Version 6 (IPv6) Specification | IPv6 |
| 11 | RFC 1918 — Address Allocation for Private Internets; RFC 4291 — IPv6 Addressing Architecture | Private/reserved ranges (validation) |
| 12 | Poese, I., et al. (2011). *IP Geolocation Databases: Unreliable?* ACM SIGCOMM CCR 41(2). | Accuracy limitation |
| 13 | Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide.* | Scrum |
| 14 | Chacon, S. & Straub, B. (2014). *Pro Git* (2nd ed.) | Git/branching |
| 15 | GitHub Docs — GitHub Actions; Jenkins Documentation — Pipeline | CI/CD |
| 16 | Flask documentation (Pallets) · Requests documentation | Implementation stack |
| 17 | pytest documentation | Testing |
| 18 | Leaflet documentation · OpenStreetMap tile usage policy | Mapping |
| 19 | OWASP API Security Top 10 (2023) | Security |
| 20 | Wiggins, A. *The Twelve-Factor App* (config in environment) | Config/secrets |

Keep extras (16–20) so you can still reach 15 if a source can't be verified. Each source gets 2–4 sentences: what it is → why it matters to IPAtlas. Group under subheadings: *Network programmability & SDN*, *IP addressing & geolocation*, *REST/JSON/HTTP & the APIs used*, *Agile, Git, CI/CD & testing*, *Security & mapping*.

## 4. Implementation — what to capture (fill from real project data)

- **Team dynamics & Agile:** Scrum Leader `[name]`, Recorder `[name]`, Developers `[…]`. Sprint length `[e.g. 1 week]`, meetings `[daily 15-min / 2×week]`, channel `[Messenger/Discord/Webex]`. Backlog source = user stories in `02-topic2-spec.md`; show board screenshot and sprint goal per sprint. Be honest about uneven workload and how it was resolved (counts as an "interpersonal challenge").
- **Architecture:** diagram from `03-architecture.md`; one paragraph per component; request-flow description.
- **Development & version control:** branching strategy, PR template, review process, merge-conflict example with screenshots, commit-message convention, contributor graph.
- **Testing & CI/CD:** test matrix (from `06-cicd-testing.md`), coverage %, Actions YAML explained, screenshot of green + one deliberately red run, Jenkins pipeline description/screenshot, how a commit triggers the pipeline.
- **UI screenshots:** normal state, IPv6 missing, invalid input, rate-limit/error banner.
- **Repo link** prominently.

## 5. Conclusion with Recommendation

- Objectives met? (table: objective → met / partly → evidence).
- Challenges and fixes: candidates — IPv6 unavailable on home network (fix: lookup-any-IP + documented limitation), free-tier rate limits (cache), mocked tests vs flaky APIs, uneven teamwork (task re-slicing).
- Recommendations: Webex notifications of lookups/builds · bulk lookup + CSV export · provider fallback (ipstack/ipinfo) · ASN/WHOIS enrichment · Docker + gunicorn + reverse proxy with TLS · rate limiting per client · Postgres + Redis cache · integration tests · monitoring.

## References

Formatted list matching in-text citations (≥ 15).

## Evidence folder (`docs/report/evidence/`)

Screenshots with dated filenames: board, PR list, a PR review, conflict resolution, Actions runs, coverage, UI states, Jenkins.
