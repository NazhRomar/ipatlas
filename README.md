# IPAtlas — IP Geolocation and Network Mapper

Python/Flask app that discovers your public IPv4 and IPv6 addresses, geolocates any IP through the ipapi.co REST API, and (MVP, in progress) shows it on a dashboard with a map. IT26210 final deliverable, Topic 2.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
copy .env.example .env   # optional
python run.py            # http://127.0.0.1:5000
```

## Test

```powershell
pytest --cov=app
flake8 app tests
```

Tests mock all HTTP; no network is needed.

## API

| Endpoint | Description |
|---|---|
| `GET /api/health` | Liveness check |
| `GET /api/myip` | Public `ipv4` / `ipv6` of this machine (`null` if unavailable) |
| `GET /api/lookup/me` | `myip` plus geolocation of the primary address |
| `GET /api/lookup/<ip>` | Geolocate any public IPv4/IPv6 |
| `GET /api/history?limit=20` | Recent lookups |
| `DELETE /api/history` | Clear history |

Errors are JSON: `{"error": {"code": "...", "message": "..."}}`.

## Docs

Project context and plans live in [CONTEXT.md](CONTEXT.md) and `docs/context/`.
