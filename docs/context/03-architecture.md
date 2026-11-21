# 03 — Architecture & Design

## High-level diagram

```mermaid
flowchart LR
    U[User / Browser<br/>Dashboard + Leaflet map] -- HTTP JSON --> F[Flask App<br/>REST API + Jinja page]
    F --> V[validators.py<br/>ipaddress module]
    F --> S[services/<br/>ipify_client, ipapi_client]
    F <--> D[(SQLite<br/>history + cache)]
    S -- HTTPS GET --> I1[ipify<br/>api.ipify.org / api6.ipify.org]
    S -- HTTPS GET --> I2[ipapi.co<br/>/{ip}/json/]
    U -- tiles --> T[OpenStreetMap tiles]
    Dev[Developers] -- push / PR --> GH[GitHub repo]
    GH -- trigger --> CI[GitHub Actions<br/>lint + pytest]
    GH -. webhook .-> J[Jenkins<br/>Jenkinsfile]
    CI -. optional .-> W[Webex Teams room]
```

(Use this same diagram — redrawn cleanly in draw.io/Figma/PowerPoint — in report Section 4 and in the video.)

## Request flow: "show my location"

1. Browser loads `/` → page JS calls `GET /api/lookup/me`.
2. Flask calls `ipify_client.get_ipv4()` and `get_ipv6()` (separate hosts, so each family is tested independently; IPv6 failure ≠ app failure).
3. For the primary IP (IPv4 if present, else IPv6) Flask checks the **cache** (SQLite, TTL e.g. 24 h).
4. Miss → `ipapi_client.lookup(ip)` → `https://ipapi.co/{ip}/json/` → parse → **normalize** to our schema.
5. Save to history/cache, return JSON.
6. Browser renders cards + moves the map pin.

## Components

| Module | Responsibility | Talks to |
|---|---|---|
| `app/__init__.py` | App factory, config, blueprint registration | all |
| `app/routes.py` | HTTP endpoints, JSON shaping, status codes | services, storage |
| `app/validators.py` | Validate/classify IP (v4/v6, private, reserved) using stdlib `ipaddress` | — |
| `app/services/ipify_client.py` | Discover public IPv4 / IPv6 | ipify (HTTPS) |
| `app/services/ipapi_client.py` | Geolocate IP, normalize response, map API errors to our exceptions | ipapi.co (HTTPS) |
| `app/storage.py` | SQLite: `lookups` table (history + cache) | sqlite3 |
| `app/errors.py` | Custom exceptions → JSON error handlers | — |
| `app/templates/index.html`, `app/static/*` | The MVP dashboard | `/api/*` |
| `tests/` | pytest suite (mocked HTTP) | — |

## Why this shape

- **Thin routes, fat services:** routes only translate HTTP ↔ Python; clients and validators hold logic → easy unit tests.
- **Backend does the outbound calls** (not the browser) so the quota, caching, validation and error mapping live in one place and can be tested; the browser only talks to our own origin (no CORS issues).
- **Normalized schema** insulates the UI from ipapi.co field changes and makes swapping to ipstack a one-file change.

## Normalized lookup schema (the contract between backend and UI)

```json
{
  "ip": "8.8.8.8",
  "version": 4,
  "city": "Mountain View",
  "region": "California",
  "country": "United States",
  "country_code": "US",
  "postal": "94035",
  "latitude": 37.386,
  "longitude": -122.0838,
  "timezone": "America/Los_Angeles",
  "org": "GOOGLE",
  "asn": "AS15169",
  "source": "ipapi.co",
  "cached": false,
  "fetched_at": "2026-11-21T10:15:00Z"
}
```

## Repo layout (target)

```
final-examination/
├─ CONTEXT.md  CLAUDE.md  README.md
├─ docs/context/            # these files
├─ docs/report/             # PDF source, diagrams, screenshots
├─ app/
│  ├─ __init__.py  routes.py  validators.py  storage.py  errors.py  config.py
│  ├─ services/ { ipify_client.py, ipapi_client.py }
│  ├─ templates/index.html
│  └─ static/ { css/style.css, js/app.js }
├─ tests/ { test_validators.py, test_ipapi_client.py, test_ipify_client.py, test_routes.py, test_storage.py }
├─ .github/workflows/ci.yml
├─ Jenkinsfile
├─ requirements.txt  requirements-dev.txt  .env.example  .gitignore
└─ run.py
```

## Tech stack summary

Python 3.11+ · Flask · requests · sqlite3 · pytest, pytest-cov, responses · flake8 (or ruff) · Leaflet 1.9 + OpenStreetMap tiles · GitHub Actions · Jenkins (Jenkinsfile).

## Where the course topics show up

| Course theme | Where in IPAtlas |
|---|---|
| REST API over HTTPS, JSON parsing | ipify/ipapi clients |
| Python | whole backend |
| Version control / social coding | branches, PRs, reviews |
| CI/CD | Actions workflow + Jenkinsfile |
| Agile/Scrum | board, sprints, roles |
| Network concepts | IPv4/IPv6, ASN, private/reserved ranges |
