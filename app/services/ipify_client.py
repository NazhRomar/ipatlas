"""Discover this machine's public IPv4 / IPv6 address via ipify (HTTPS)."""
from typing import Optional

import requests

from ..errors import InvalidIPError, UpstreamError, UpstreamTimeout
from ..validators import parse_ip

USER_AGENT = "IPAtlas/1.0 (student project)"


def _fetch(url: str, timeout: float, version: int) -> str:
    """GET the ipify JSON endpoint and return an address of the given family."""
    try:
        resp = requests.get(
            url,
            params={"format": "json"},
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
        resp.raise_for_status()
        raw = resp.json().get("ip")
    except requests.Timeout:
        raise UpstreamTimeout("ipify timed out.") from None
    except (requests.RequestException, ValueError, AttributeError):
        raise UpstreamError("ipify returned an unexpected response.") from None
    try:
        ip = parse_ip(raw)
    except InvalidIPError:
        raise UpstreamError("ipify returned an invalid address.") from None
    if ip.version != version:
        raise UpstreamError(f"ipify returned an IPv{ip.version} address, expected IPv{version}.")
    return str(ip)


def get_ipv4(url: str, timeout: float) -> str:
    """Return the public IPv4 address. Raises UpstreamError on any failure."""
    return _fetch(url, timeout, 4)


def get_ipv6(url: str, timeout: float) -> Optional[str]:
    """Return the public IPv6 address, or None if this network has no IPv6.

    Many networks lack IPv6 entirely, so connection failures, timeouts and
    bad responses are treated as "not available" rather than as errors.
    """
    try:
        return _fetch(url, timeout, 6)
    except UpstreamError:
        return None
