import requests
import responses

IPIFY_V4 = "https://api.ipify.org"
IPIFY_V6 = "https://api6.ipify.org"
IPAPI_8888 = "https://ipapi.co/8.8.8.8/json/"


def test_t16_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_index_page(client):
    assert client.get("/").status_code == 200


@responses.activate
def test_t17_lookup_success(client, sample_ipapi):
    responses.add(responses.GET, IPAPI_8888, json=sample_ipapi)
    resp = client.get("/api/lookup/8.8.8.8")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ip"] == "8.8.8.8"
    assert body["city"] == "Mountain View"
    assert body["cached"] is False


def test_t18_invalid_ip(client):
    resp = client.get("/api/lookup/abc")
    assert resp.status_code == 400
    assert resp.get_json()["error"]["code"] == "invalid_ip"


def test_private_ip_makes_no_upstream_call(client):
    with responses.RequestsMock() as rsps:  # fails if any request is made
        resp = client.get("/api/lookup/192.168.1.1")
        assert len(rsps.calls) == 0
    assert resp.status_code == 422
    assert resp.get_json()["error"]["code"] == "reserved_ip"


@responses.activate
def test_t19_second_lookup_is_cached(client, sample_ipapi):
    responses.add(responses.GET, IPAPI_8888, json=sample_ipapi)
    first = client.get("/api/lookup/8.8.8.8").get_json()
    second = client.get("/api/lookup/8.8.8.8").get_json()
    assert first["cached"] is False
    assert second["cached"] is True
    assert len(responses.calls) == 1


@responses.activate
def test_ipv6_lookup_route(client, sample_ipapi):
    payload = {**sample_ipapi, "ip": "2001:4860:4860::8888", "version": "IPv6"}
    responses.add(
        responses.GET, "https://ipapi.co/2001:4860:4860::8888/json/", json=payload
    )
    resp = client.get("/api/lookup/2001:4860:4860:0:0:0:0:8888")  # non-compressed form
    assert resp.status_code == 200
    assert resp.get_json()["version"] == 6


@responses.activate
def test_rate_limit_maps_to_429(client):
    responses.add(responses.GET, IPAPI_8888, status=429)
    resp = client.get("/api/lookup/8.8.8.8")
    assert resp.status_code == 429
    assert resp.get_json()["error"]["code"] == "rate_limited"


@responses.activate
def test_upstream_timeout_maps_to_504(client):
    responses.add(responses.GET, IPAPI_8888, body=requests.exceptions.Timeout("slow"))
    resp = client.get("/api/lookup/8.8.8.8")
    assert resp.status_code == 504
    assert resp.get_json()["error"]["code"] == "upstream_timeout"


@responses.activate
def test_myip_both(client):
    responses.add(responses.GET, IPIFY_V4, json={"ip": "8.8.8.8"})
    responses.add(responses.GET, IPIFY_V6, json={"ip": "2001:4860:4860::8888"})
    assert client.get("/api/myip").get_json() == {
        "ipv4": "8.8.8.8", "ipv6": "2001:4860:4860::8888",
    }


@responses.activate
def test_myip_both_fail_is_502(client):
    responses.add(responses.GET, IPIFY_V4, status=500)
    responses.add(responses.GET, IPIFY_V6, body=requests.exceptions.ConnectionError("x"))
    resp = client.get("/api/myip")
    assert resp.status_code == 502


@responses.activate
def test_t20_lookup_me_without_ipv6(client, sample_ipapi):
    responses.add(responses.GET, IPIFY_V4, json={"ip": "8.8.8.8"})
    responses.add(responses.GET, IPIFY_V6, body=requests.exceptions.ConnectionError("no v6"))
    responses.add(responses.GET, IPAPI_8888, json=sample_ipapi)
    resp = client.get("/api/lookup/me")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ipv4"] == "8.8.8.8"
    assert body["ipv6"] is None
    assert body["location"]["country_code"] == "US"


@responses.activate
def test_lookup_me_ipv6_only_uses_ipv6(client, sample_ipapi):
    v6 = "2001:4860:4860::8888"
    responses.add(responses.GET, IPIFY_V4, status=500)
    responses.add(responses.GET, IPIFY_V6, json={"ip": v6})
    responses.add(
        responses.GET, f"https://ipapi.co/{v6}/json/", json={**sample_ipapi, "ip": v6}
    )
    body = client.get("/api/lookup/me").get_json()
    assert body["ipv4"] is None
    assert body["location"]["version"] == 6


@responses.activate
def test_history_and_clear(client, sample_ipapi):
    responses.add(responses.GET, IPAPI_8888, json=sample_ipapi)
    client.get("/api/lookup/8.8.8.8")
    history = client.get("/api/history").get_json()
    assert [h["ip"] for h in history] == ["8.8.8.8"]
    assert client.delete("/api/history").status_code == 204
    assert client.get("/api/history").get_json() == []


def test_history_bad_limit(client):
    for bad in ("abc", "0", "101"):
        resp = client.get(f"/api/history?limit={bad}")
        assert resp.status_code == 400
        assert resp.get_json()["error"]["code"] == "invalid_parameter"


def test_unknown_api_route_returns_json_404(client):
    resp = client.get("/api/nope")
    assert resp.status_code == 404
    assert "error" in resp.get_json()
