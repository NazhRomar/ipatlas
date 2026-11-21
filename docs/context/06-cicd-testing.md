# 06 — Testing, CI/CD & Git Workflow

## Test strategy

- **Unit tests (pytest)** for validators, clients (mocked HTTP), storage (temp DB), routes (Flask test client).
- **No live network in CI.** Mock with `responses` (or `unittest.mock.patch` on `requests.get`).
- Target ≥ 80% coverage on `app/` (report the number in the documentation).
- One optional **manual smoke test** with live APIs before the demo.

### Test case matrix (write these first — they double as the report's "test plan")

| ID | Unit | Case | Expect |
|---|---|---|---|
| T01 | validators | `8.8.8.8` | IPv4 object, `is_global` true |
| T02 | validators | `2001:4860:4860::8888` | IPv6 object |
| T03 | validators | `999.1.1.1`, `abc`, `""`, `None`, ` 8.8.8.8 ` (spaces) | `InvalidIPError` ×4, trimmed OK |
| T04 | validators | `192.168.1.1`, `10.0.0.1`, `127.0.0.1`, `::1`, `169.254.1.1` | `ReservedIPError` |
| T05 | ipify | v4 success JSON | returns string |
| T06 | ipify | v6 connection error | returns `None` |
| T07 | ipify | timeout on v4 | `UpstreamTimeout` |
| T08 | ipapi | valid JSON → normalize | all schema keys present, types right |
| T09 | ipapi | JSON with missing fields | `null`s, no `KeyError` |
| T10 | ipapi | `{"error":true,"reason":"Reserved IP Address"}` | `ReservedIPError` |
| T11 | ipapi | HTTP 429 | `RateLimitError` |
| T12 | ipapi | HTTP 500 / bad JSON | `UpstreamError` |
| T13 | storage | save → get_cached within TTL | hit |
| T14 | storage | get_cached after TTL | miss |
| T15 | storage | `recent(limit)` ordering | newest first |
| T16 | routes | `GET /api/health` | 200 `ok` |
| T17 | routes | `GET /api/lookup/8.8.8.8` (mocked) | 200 schema |
| T18 | routes | `GET /api/lookup/abc` | 400 error shape |
| T19 | routes | second lookup same IP | `cached: true`, upstream called once |
| T20 | routes | `GET /api/lookup/me` with v6 missing | 200, `ipv6: null` |

## GitHub Actions — `.github/workflows/ci.yml`

```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: flake8 app tests --max-line-length=100
      - run: pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

Add the badge to README: `![CI](https://github.com/<user>/<repo>/actions/workflows/ci.yml/badge.svg)`.
(Check the current major versions of the `actions/*` steps when creating the file.)

## Jenkins — `Jenkinsfile` (declarative)

```groovy
pipeline {
  agent any
  triggers { githubPush() }          // needs GitHub webhook -> Jenkins
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Setup')    { steps { sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt' } }
    stage('Lint')     { steps { sh '. .venv/bin/activate && flake8 app tests --max-line-length=100' } }
    stage('Test')     { steps { sh '. .venv/bin/activate && pytest --junitxml=report.xml --cov=app' } }
  }
  post {
    always  { junit 'report.xml' }
    success { echo 'Build passed' }
    failure { echo 'Build FAILED' }   // optional stretch: curl a Webex webhook here
  }
}
```

Jenkins needs a reachable machine (a laptop or small VM; webhook delivery from GitHub needs a public URL, e.g. via a tunnel). If that's too heavy, **GitHub Actions is the primary pipeline** and the Jenkinsfile is kept as the documented Jenkins equivalent; say so honestly in Limitations. Open question #3 in `CONTEXT.md` decides how much effort Jenkins deserves.

## Git workflow (evidence for report §4 "Development & Version Control")

- **Branches:** `main` (always demoable, protected) ← `develop` ← `feature/<short-name>` (e.g. `feature/ipapi-client`, `feature/dashboard-map`), `fix/…`, `docs/…`.
- **Commits:** Conventional style — `feat:`, `fix:`, `test:`, `docs:`, `ci:`, `chore:`.
- **PRs:** small, linked to a board item, template with checklist (tests added, CI green, screenshot for UI changes). **≥1 teammate review** before merge; use "Squash and merge" or merge commit consistently.
- **Branch protection on `main`:** require PR + passing CI status check.
- **Merge conflict story:** plan one deliberately natural case (two people touching `README.md` or `requirements.txt`), resolve it, and screenshot the conflict + resolution — the rubric explicitly asks how conflicts were handled.
- **Issue tracking:** GitHub Issues + GitHub Projects Kanban (Backlog → Sprint → In progress → Review → Done).

## `.gitignore` essentials

`.venv/`, `__pycache__/`, `.env`, `instance/`, `*.db`, `.coverage`, `htmlcov/`, `.pytest_cache/`, `report.xml`.

## Requirements files

- `requirements.txt`: `Flask`, `requests`, `python-dotenv` (pin versions after first working install via `pip freeze`).
- `requirements-dev.txt`: `pytest`, `pytest-cov`, `responses`, `flake8`.
