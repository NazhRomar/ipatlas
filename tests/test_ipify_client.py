import pytest
import requests
import responses

from app.errors import UpstreamError, UpstreamTimeout
from app.services import ipify_client

V4 = "https://api.ipify.org"
V6 = "https://api6.ipify.org"


@responses.activate
def test_t05_ipv4_success():
    responses.add(responses.GET, V4, json={"ip": "203.0.113.9"})
    # 203.0.113.0/24 is a documentation range but still a valid IPv4 literal
    assert ipify_client.get_ipv4(V4, 5) == "203.0.113.9"


@responses.activate
def test_t06_ipv6_connection_error_returns_none():
    responses.add(responses.GET, V6, body=requests.exceptions.ConnectionError("no v6"))
    assert ipify_client.get_ipv6(V6, 5) is None


@responses.activate
def test_ipv6_success():
    responses.add(responses.GET, V6, json={"ip": "2001:4860:4860::8888"})
    assert ipify_client.get_ipv6(V6, 5) == "2001:4860:4860::8888"


@responses.activate
def test_t07_ipv4_timeout_raises():
    responses.add(responses.GET, V4, body=requests.exceptions.Timeout("slow"))
    with pytest.raises(UpstreamTimeout):
        ipify_client.get_ipv4(V4, 5)


@responses.activate
def test_ipv4_http_error_raises():
    responses.add(responses.GET, V4, status=500)
    with pytest.raises(UpstreamError):
        ipify_client.get_ipv4(V4, 5)


@responses.activate
def test_ipv4_wrong_family_raises():
    responses.add(responses.GET, V4, json={"ip": "2001:db8::1"})
    with pytest.raises(UpstreamError):
        ipify_client.get_ipv4(V4, 5)


@responses.activate
def test_ipv4_garbage_body_raises():
    responses.add(responses.GET, V4, body="not json", status=200)
    with pytest.raises(UpstreamError):
        ipify_client.get_ipv4(V4, 5)
