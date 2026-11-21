# 04 — Backend Specification

## API contract

Base: `http://127.0.0.1:5000`. All `/api/*` responses are JSON. Errors share one shape:

```json
{ "error": { "code": "invalid_ip", "message": "'999.1.1.1' is not a valid IPv4 or IPv6 address." } }
```

| Method & path | Purpose | Success | Errors |
|---|---|---|---|
| `GET /` | Dashboard page | 200 HTML | — |
| `GET /api/health` | Liveness check (also used by CI smoke test) | 200 `{"status":"ok"}` | — |
| `GET /api/myip` | Public addresses of this client | 200 `{"ipv4":"1.2.3.4"\|null,"ipv6":"..."\|null}` | 502 `upstream_error` only if **both** fail |
| `GET /api/lookup/me` | `myip` + geolocation of the primary IP (v4, else v6) | 200 `{ "ipv4":…, "ipv6":…, "location": <schema> }` | 502 / 429 |
| `GET /api/lookup/<ip>` | Geolocate any IP | 200 `<schema>` | 400 `invalid_ip`, 422 `reserved_ip`, 429 `rate_limited`, 502 `upstream_error`, 504 `upstream_timeout` |
| `GET /api/history?limit=20` | Recent lookups, newest first | 200 `[<schema>…]` | 400 on bad limit |
| `DELETE /api/history` | Clear history (optional) | 204 | — |

Schema = normalized lookup object in `03-architecture.md`.

## Module behavior

### `validators.py`
- `parse_ip(raw) -> ipaddress.IPv4Address | IPv6Address` — strip whitespace; raise `InvalidIPError`.
- `classify(ip)` → `{"version": 4|6, "is_private", "is_loopback", "is_reserved", "is_global"}`.
- Reject private/loopback/link-local/reserved for geolocation with `ReservedIPError` (ipapi.co would just return a "Reserved IP" error anyway; failing early saves quota).
- Use only stdlib `ipaddress` — don't hand-roll regexes.

### `services/ipify_client.py`
- `get_ipv4()` → `GET https://api.ipify.org?format=json`; `get_ipv6()` → `GET https://api6.ipify.org?format=json`.
- Timeout 5 s. On `ConnectionError`/timeout for IPv6 return `None` (not an error: many networks have no IPv6). Verify the returned string really is the right family via `validators`.

### `services/ipapi_client.py`
- `lookup(ip)` → `GET https://ipapi.co/{ip}/json/`, `User-Agent: IPAtlas/1.0 (student project)` (generic — **no personal data in headers**).
- ipapi.co signals failures inside the JSON body (`{"error": true, "reason": "..."}`) and with HTTP 429 for rate limits → translate to `ReservedIPError`, `RateLimitError`, `UpstreamError`.
- `normalize(raw) -> dict` maps `country_name→country`, `org→org`, `asn→asn`, etc. Missing fields become `null`, never `KeyError`.
- Verify field names against the live docs at implementation time (https://ipapi.co/api/) — free-tier fields/limits change.

### `storage.py`
- Table `lookups(id INTEGER PK, ip TEXT, payload TEXT /*JSON*/, fetched_at TEXT)`; index on `ip`.
- `get_cached(ip, ttl_seconds)`, `save(ip, payload)`, `recent(limit)`, `clear()`.
- Parameterized queries only (no f-string SQL). DB path from config; tests use `:memory:` / tmp path.

### `errors.py`
Exception hierarchy → `@app.errorhandler` mapping to the JSON error shape and status codes above:
`InvalidIPError(400)`, `ReservedIPError(422)`, `RateLimitError(429)`, `UpstreamTimeout(504)`, `UpstreamError(502)`.

### Client IP behind a proxy
`/api/lookup/me` discovers IPs by calling ipify **from the server**. On a local demo that equals the user's public IP. If ever deployed, use `X-Forwarded-For` (only when behind a trusted proxy) — document in Limitations; don't build now.

## Configuration (`config.py` + `.env`)

| Variable | Default | Meaning |
|---|---|---|
| `IPAPI_BASE_URL` | `https://ipapi.co` | Swap provider/mock |
| `IPAPI_KEY` | *(empty)* | Optional paid key; never committed |
| `HTTP_TIMEOUT` | `5` | Seconds, all outbound calls |
| `CACHE_TTL` | `86400` | Seconds |
| `DB_PATH` | `instance/ipatlas.db` | SQLite file (git-ignored) |
| `FLASK_DEBUG` | `0` | Only `1` locally |

## Security checklist (cite OWASP API Top 10 in report)

- [ ] Input validated server-side before any outbound call (blocks SSRF-style abuse: only IP literals, never hostnames/URLs)
- [ ] HTTPS-only outbound, timeouts, response size sanity (JSON only)
- [ ] No secrets in repo; `.env` ignored; `.env.example` committed
- [ ] Parameterized SQL
- [ ] Jinja autoescape on; no `innerHTML` with API data in the frontend (use `textContent`)
- [ ] Debug mode off by default
- [ ] Generic User-Agent; no personal data sent to third parties

## Python conventions

Type hints, docstrings on public functions, `flake8`/`ruff` clean, no print debugging (use `logging`), functions small enough to unit test.
