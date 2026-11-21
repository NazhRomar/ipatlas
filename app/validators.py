"""IP address validation and classification (stdlib `ipaddress` only)."""
import ipaddress
from typing import Union

from .errors import InvalidIPError, ReservedIPError

IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]


def parse_ip(raw: object) -> IPAddress:
    """Parse user input into an IP address object or raise InvalidIPError."""
    if not isinstance(raw, str) or not raw.strip():
        raise InvalidIPError("An IP address is required.")
    text = raw.strip()
    try:
        return ipaddress.ip_address(text)
    except ValueError:
        shown = text if len(text) <= 64 else text[:64] + "..."
        raise InvalidIPError(
            f"'{shown}' is not a valid IPv4 or IPv6 address."
        ) from None


def classify(ip: IPAddress) -> dict:
    """Describe an address: version and which special range it belongs to."""
    return {
        "version": ip.version,
        "is_private": ip.is_private,
        "is_loopback": ip.is_loopback,
        "is_link_local": ip.is_link_local,
        "is_reserved": ip.is_reserved,
        "is_global": ip.is_global,
    }


def ensure_public(ip: IPAddress) -> IPAddress:
    """Raise ReservedIPError unless the address is publicly routable."""
    if not ip.is_global:
        raise ReservedIPError(
            f"{ip} is a private or reserved address and cannot be geolocated."
        )
    return ip
