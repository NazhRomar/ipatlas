# 05 — MVP: Dashboard UI Specification

The MVP is the thing graders *see* in the demo, so it must look clean and never show a raw error.

## Tech

Server-rendered `index.html` (Jinja) + `static/css/style.css` + `static/js/app.js` (vanilla JS, `fetch`). Map: **Leaflet 1.9.x** from a CDN with an exact pinned version + OpenStreetMap tiles (keep the attribution). No build step, no framework — fewer things to break on demo day.

## Layout (desktop; stacks vertically on mobile)

```
┌──────────────────────────────────────────────────────────────┐
│  IPAtlas  ·  IP Geolocation & Network Mapper        [theme]  │
├───────────────┬───────────────┬──────────────────────────────┤
│  YOUR IPv4    │  YOUR IPv6    │  Lookup any IP               │
│  1.2.3.4      │  2001:db8::1  │  [ 8.8.8.8            ][Go]  │
│  [copy]       │  or "Not      │  hint: IPv4 or IPv6          │
│               │  detected"    │                              │
├───────────────┴───────────────┴──────────────────────────────┤
│  LOCATION DETAILS                │          MAP              │
│  City / Region / Country  flag?  │   (Leaflet, pin + popup)  │
│  Lat, Lon · Timezone             │                           │
│  ISP/Org · ASN · IP version      │                           │
│  source · cached? · fetched_at   │                           │
├──────────────────────────────────┴───────────────────────────┤
│  RECENT LOOKUPS  (table: time · IP · v · city, country)      │
│  click a row → re-show on map          [Clear history]       │
└──────────────────────────────────────────────────────────────┘
```

## Behavior

| Event | Result |
|---|---|
| Page load | Skeleton/“Loading…” in cards → `GET /api/lookup/me` → fill IPv4/IPv6 cards, location card, map pin; load history |
| IPv6 missing | IPv6 card shows muted "Not detected on this network" (not red) |
| Submit lookup | Client-side trim; `GET /api/lookup/<ip>`; disable button while pending; update details + map + history |
| Click history row | Re-render details + map from the stored payload (no new API call needed) |
| Copy button | `navigator.clipboard.writeText`, brief "Copied" |
| Error (400/422/429/502/504) | Inline banner under the input using `error.message` — amber for user mistakes (400/422), red for upstream issues |
| Missing lat/lon | Show details, hide the pin, note "No coordinates returned" |

## Visual style

- Neutral background, one accent color, cards with soft borders, 16px base font, large IP text (monospace) so it's legible in a screen recording.
- Color-code version badges: IPv4 / IPv6 chips.
- Support `prefers-color-scheme: dark`.
- Accessible: labels on inputs, sufficient contrast, keyboard submit with Enter.

## Frontend safety/quality

- Insert API data with `textContent`, never `innerHTML`.
- One `render(location)` function used by both "me" and "lookup" paths.
- All fetches via a small `api(path)` helper that throws on `!ok` with the server's `error.message`.
- No inline secrets; no external calls other than our own `/api/*`, Leaflet CDN assets, and OSM tiles.

## Demo-friendly extras (cheap, high-impact)

- Preset chips: `8.8.8.8`, `1.1.1.1`, `2001:4860:4860::8888` (IPv6 demo even without native IPv6), `invalid` example.
- Footer: GitHub repo link + CI badge.

## Stretch UI (only after MVP is solid)

Compare IPv4 vs IPv6 side by side · multi-IP network map with several pins · CSV/JSON export · dark-mode toggle button.

## Acceptance checks (manual, run before recording the video)

- [ ] Fresh page load < 3 s on normal Wi-Fi
- [ ] `8.8.8.8` and `2001:4860:4860::8888` both pin the map
- [ ] `999.1.1.1`, `abc`, `192.168.1.1`, `127.0.0.1` show friendly messages
- [ ] Airplane-mode / blocked network shows the upstream error banner, page doesn't break
- [ ] Reload shows history persisted
- [ ] Works at 1280×720 (recording resolution) and on a phone-width window
