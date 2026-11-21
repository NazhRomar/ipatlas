"""Geolocate an IP address via ipapi.co (HTTPS) and normalize the response."""
import ipaddress
from datetime import datetime, timezone
from typing import Optional

import requests

from ..errors import RateLimitError, ReservedIPError, UpstreamError, UpstreamTimeout

USER_AGENT = "IPAtlas/1.0 (student project)"


def _to_float(value: object) -> Optional[float]:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _version_of(ip: Optional[str]) -> Optional[int]:
    try:
        return ipaddress.ip_address(ip).version  # type: ignore[arg-type]
    except ValueError:
        return None


def normalize(raw: dict, requested_ip: Optional[str] = None) -> dict:
    """Map an ipapi.co JSON object to IPAtlas's schema. Missing fields become None."""
    ip = raw.get("ip") or requested_ip
    return {
        "ip": ip,
        "version": _version_of(ip),
        "city": raw.get("city"),
        "region": raw.get("region"),
        "country": raw.get("country_name"),
        "country_code": raw.get("country_code"),
        "postal": raw.get("postal"),
        "latitude": _to_float(raw.get("latitude")),
        "longitude": _to_float(raw.get("longitude")),
        "timezone": raw.get("timezone"),
        "org": raw.get("org"),
        "asn": raw.get("asn"),
        "source": "ipapi.co",
        "cached": False,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def lookup(ip: str, base_url: str, timeout: float, api_key: str = "") -> dict:
    """Fetch and normalize geolocation data for `ip`.

    ipapi.co reports some failures inside a JSON body ({"error": true, ...})
    and rate limits with HTTP 429; both are mapped to IPAtlas exceptions.
    """
    url = f"{base_url.rstrip('/')}/{ip}/json/"
    params = {"key": api_key} if api_key else None
    try:
        resp = requests.get(
            url,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
    except requests.Timeout:
        raise UpstreamTimeout("ipapi.co timed out.") from None
    except requests.RequestException:
        raise UpstreamError("Could not reach ipapi.co.") from None

    if resp.status_code == 429:
        raise RateLimitError()
    if resp.status_code >= 400:
        raise UpstreamError(f"ipapi.co returned HTTP {resp.status_code}.")

    try:
        raw = resp.json()
    except ValueError:
        raise UpstreamError("ipapi.co returned invalid JSON.") from None
    if not isinstance(raw, dict):
        raise UpstreamError("ipapi.co returned an unexpected payload.")

    if raw.get("error"):
        reason = str(raw.get("reason", "unknown error"))
        lowered = reason.lower()
        if "reserved" in lowered:
            raise ReservedIPError(f"{ip} is a private or reserved address.")
        if "rate" in lowered or "quota" in lowered:
            raise RateLimitError()
        raise UpstreamError(f"ipapi.co error: {reason}")

    return normalize(raw, requested_ip=ip)
