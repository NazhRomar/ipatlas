import ipaddress

import pytest

from app.errors import InvalidIPError, ReservedIPError
from app.validators import classify, ensure_public, parse_ip


def test_t01_parses_ipv4():
    ip = parse_ip("8.8.8.8")
    assert isinstance(ip, ipaddress.IPv4Address)
    assert classify(ip)["is_global"] is True


def test_t02_parses_ipv6():
    ip = parse_ip("2001:4860:4860::8888")
    assert isinstance(ip, ipaddress.IPv6Address)
    assert classify(ip)["version"] == 6


@pytest.mark.parametrize("bad", ["999.1.1.1", "abc", "", "   ", None, 123, "8.8.8"])
def test_t03_rejects_invalid(bad):
    with pytest.raises(InvalidIPError):
        parse_ip(bad)


def test_t03_trims_whitespace():
    assert str(parse_ip("  8.8.8.8  ")) == "8.8.8.8"


@pytest.mark.parametrize(
    "addr", ["192.168.1.1", "10.0.0.1", "127.0.0.1", "::1", "169.254.1.1", "fe80::1"]
)
def test_t04_rejects_private_and_reserved(addr):
    with pytest.raises(ReservedIPError):
        ensure_public(parse_ip(addr))


def test_ensure_public_returns_address():
    ip = parse_ip("1.1.1.1")
    assert ensure_public(ip) == ip


def test_long_invalid_input_is_truncated_in_message():
    with pytest.raises(InvalidIPError) as excinfo:
        parse_ip("x" * 500)
    assert len(excinfo.value.message) < 200
