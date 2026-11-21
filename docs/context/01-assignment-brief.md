# 01 — Assignment Brief (condensed rubric)

Source: IT26210 Alternative Assessment — Final Deliverable Guidelines. Our topic: **#2 IP Geolocation and Network Mapper** (raffled).

> Topic 2: *Based on the Option 2 project choice, students build a new application using Python to retrieve users' IPv4 and IPv6 addresses via REST APIs like ipapi.co or ipstack.com. The app can output the IP's geographical location and format it into a clean UI dashboard, with tracking via a GitHub CI/CD pipeline.*

The overall course project is a five-part workplace simulation: Agile (Scrum) roles, Python, Git version control, REST over HTTPS, CI/CD (Jenkins), and network programmability (NETCONF / Webex Teams API). Topic 2 only *needs* REST + Python + Git + CI/CD; NETCONF/Webex are not required for this topic (Webex notification is an optional stretch).

## Deliverable 1 — Formal documentation (PDF)

Format: **PDF, 12pt, single-spaced, headings, title page.** Include the public GitHub URL in the document.

| # | Section | What the rubric wants |
|---|---|---|
| 1 | **Objectives** | 1 General Objective + **3–5** Specific Objectives (technical milestones) |
| 2 | **Scopes and Limitations** | Scope: APIs used, devices targeted, UI type (CLI vs GUI), Agile methods applied. Limitations: what's excluded / backlog |
| 3 | **Related Literatures** | **≥ 15 sources.** Cover: network programmability & SDN; docs of APIs integrated (ipapi.co, ipify…); CI/CD, Agile/Scrum (and YANG if relevant) |
| 4 | **Implementation** | Team dynamics & Agile (Scrum Leader? Recorder? sprint planning, backlog) · System architecture diagram (code ↔ APIs ↔ devices ↔ GitHub) · Dev & version control (branching, merge conflicts, code review) · Testing & CI/CD (test plan, unit tests, pipeline on commit) |
| 5 | **Conclusion with Recommendation** | Did we meet objectives? Challenges (technical + interpersonal) and fixes. Next features; optimization/scaling |

## Deliverable 2 — Video pitch (5–10 min, all members on camera/voice)

| Segment | Must show / say |
|---|---|
| 1. Intro & roles | Project name + value proposition; each proponent introduced with explicit role |
| 2. How it was made | Agile journey (meeting frequency, communication channel); screen share of GitHub repo / backlog / Kanban board |
| 3. Implementation breakdown | **Each member** explains the part *they* implemented; one specific bug or team issue + the fix |
| 4. Live demo | Narrated live run; proof of functionality; short **code glimpse** of a critical snippet |

For our topic, "proof of functionality" = dashboard showing the user's IPv4/IPv6 + location on a map, **and** a commit/PR to GitHub triggering a green CI run.

Format: MP4 or unlisted YouTube/Vimeo link; clear audio, legible screen shares. Put the **GitHub link in the video description**.

## Deliverable 3 — Repository

- Public GitHub repo, link in the PDF and the video description.
- Well-written `README.md` (what it is, setup, run, test, screenshots, API, team, CI badge).

## Grading-risk checklist

- [ ] ≥15 real, citable literature sources (not just URLs to homepages)
- [ ] Architecture diagram present in section 4
- [ ] Scrum Leader and Recorder named explicitly
- [ ] Evidence of branching + PRs + reviews + at least one resolved merge conflict story
- [ ] Unit tests exist, pass, and run automatically on commit
- [ ] Every member speaks in video about a **real** contribution
- [ ] Repo link in both PDF and video description
- [ ] Title page, 12pt, single-spaced, PDF
