import pytest
import requests
import responses

from app.errors import RateLimitError, ReservedIPError, UpstreamError, UpstreamTimeout
from app.services import ipapi_client

BASE = "https://ipapi.co"
URL = f"{BASE}/8.8.8.8/json/"

SCHEMA_KEYS = {
    "ip", "version", "city", "region", "country", "country_code", "postal",
    "latitude", "longitude", "timezone", "org", "asn", "source", "cached", "fetched_at",
}


def test_t08_normalize_full_payload(sample_ipapi):
    out = ipapi_client.normalize(sample_ipapi)
    assert set(out) == SCHEMA_KEYS
    assert out["country"] == "United States"
    assert out["version"] == 4
    assert out["latitude"] == pytest.approx(37.386)
    assert out["source"] == "ipapi.co"
    assert out["cached"] is False


def test_t09_normalize_missing_fields_become_none():
    out = ipapi_client.normalize({}, requested_ip="2001:4860:4860::8888")
    assert set(out) == SCHEMA_KEYS
    assert out["city"] is None
    assert out["latitude"] is None
    assert out["ip"] == "2001:4860:4860::8888"
    assert out["version"] == 6


def test_normalize_non_numeric_coordinates():
    out = ipapi_client.normalize({"ip": "8.8.8.8", "latitude": "n/a", "longitude": None})
    assert out["latitude"] is None and out["longitude"] is None


@responses.activate
def test_lookup_success(sample_ipapi):
    responses.add(responses.GET, URL, json=sample_ipapi)
    out = ipapi_client.lookup("8.8.8.8", BASE, 5)
    assert out["city"] == "Mountain View"


@responses.activate
def test_lookup_sends_key_when_configured(sample_ipapi):
    responses.add(responses.GET, URL, json=sample_ipapi)
    ipapi_client.lookup("8.8.8.8", BASE, 5, api_key="secret")
    assert "key=secret" in responses.calls[0].request.url


@responses.activate
def test_t10_reserved_ip_error_body():
    responses.add(responses.GET, URL, json={"error": True, "reason": "Reserved IP Address"})
    with pytest.raises(ReservedIPError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_t11_http_429():
    responses.add(responses.GET, URL, status=429)
    with pytest.raises(RateLimitError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_rate_limit_error_body():
    responses.add(responses.GET, URL, json={"error": True, "reason": "RateLimited"})
    with pytest.raises(RateLimitError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_t12_http_500():
    responses.add(responses.GET, URL, status=500)
    with pytest.raises(UpstreamError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_t12_bad_json():
    responses.add(responses.GET, URL, body="<html>oops</html>", status=200)
    with pytest.raises(UpstreamError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_unknown_error_reason():
    responses.add(responses.GET, URL, json={"error": True, "reason": "Something odd"})
    with pytest.raises(UpstreamError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_timeout():
    responses.add(responses.GET, URL, body=requests.exceptions.Timeout("slow"))
    with pytest.raises(UpstreamTimeout):
        ipapi_client.lookup("8.8.8.8", BASE, 5)


@responses.activate
def test_connection_error():
    responses.add(responses.GET, URL, body=requests.exceptions.ConnectionError("down"))
    with pytest.raises(UpstreamError):
        ipapi_client.lookup("8.8.8.8", BASE, 5)
