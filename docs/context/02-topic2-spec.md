# 02 — Topic 2 Specification: IPAtlas

## Problem statement

Network engineers and support staff often need to answer "where is this IP, who owns it, and is it IPv4 or IPv6?" quickly. Doing it by hand across several websites is slow and inconsistent. IPAtlas discovers the user's public IPv4 and IPv6 addresses, geolocates any IP through a REST API, and presents the result on a clean dashboard with a map, while a CI/CD pipeline keeps the code tested.

## Functional requirements

| ID | Requirement | MVP? |
|---|---|---|
| F1 | Detect and display the user's **public IPv4** address | ✅ |
| F2 | Detect and display the user's **public IPv6** address (or "not available") | ✅ |
| F3 | Geolocate an IP via ipapi.co: city, region, country, lat/lon, timezone, ISP/org, ASN | ✅ |
| F4 | Lookup **any** IPv4/IPv6 typed by the user, with input validation | ✅ |
| F5 | Dashboard: cards for IPv4 / IPv6 / location details + interactive map pin | ✅ |
| F6 | Lookup history (last N) persisted in SQLite, click to re-show | ✅ |
| F7 | Friendly error states: invalid IP, private/reserved IP, rate-limited, API down, no IPv6 | ✅ |
| F8 | Cache recent lookups (TTL) to protect the free-tier quota | ✅ (simple) |
| F9 | CI pipeline on every push/PR: install → lint → unit tests; badge in README | ✅ |
| F10 | Jenkinsfile equivalent pipeline | ✅ (file + screenshot if Jenkins available) |
| F11 | Compare IPv4 vs IPv6 location side by side | Stretch |
| F12 | Export history as CSV/JSON | Stretch |
| F13 | Post lookup / build status to Webex Teams room | Stretch |
| F14 | Dark mode, units/locale toggle | Stretch |
| F15 | Multi-IP "network map" (plot several IPs at once) | Stretch |

## Non-functional requirements

- **HTTPS only** for outbound API calls; timeouts on every request (e.g. 5 s) and 1 retry max.
- **No secrets in the repo.** Optional keys via `.env`.
- **Testable:** all outbound HTTP isolated in client modules, mockable.
- **Responsive UI**, readable on projector for the demo (large type, high contrast).
- **Run in < 3 commands** from a fresh clone (documented in README).

## User stories (backlog seed — copy into GitHub Projects)

1. As a support engineer, I want to see my public IPv4 and IPv6 so I can report them to a vendor.
2. As a support engineer, I want to type any IP and see its location and ISP so I can triage an alert.
3. As a user, I want a map pin for the location so I understand it at a glance.
4. As a user, I want clear messages when something fails so I'm not staring at a stack trace.
5. As a user, I want to see my previous lookups so I don't repeat them.
6. As a developer, I want tests to run automatically on each push so regressions are caught.
7. As the scrum leader, I want a visible backlog/Kanban board so progress is traceable.

## MVP definition (done = all true)

- `py -m flask run` (or `python -m app`) serves a dashboard at `http://127.0.0.1:5000`.
- Page load shows IPv4 and IPv6 (or "not detected") and geolocation card + map for the user's primary IP.
- Typing `8.8.8.8` and `2001:4860:4860::8888` both return a location and update the map.
- Invalid input (`999.1.1.1`, `abc`) shows a clear message, not an error page.
- History list shows last lookups and survives restart.
- `pytest` passes locally and in GitHub Actions; README badge is green.

## Out of scope (goes into "Limitations")

- No NETCONF / device config (that is Topics 3, 4, 8).
- No user accounts/authentication, no multi-tenant hosting.
- Geolocation accuracy is whatever ipapi.co returns (IP geolocation is approximate by nature; city-level at best, often ISP hub).
- No paid-tier features (bulk, high quota, security/threat data).
- Production hardening (WSGI server, TLS termination, rate limiting per user) is documented but not deployed.
- Lab/demo scope: single instance, local or small VM.
