"""HTTP endpoints. Thin: translate requests to service/storage calls."""
from flask import Blueprint, current_app, jsonify, render_template, request

from . import storage
from .errors import InvalidParameterError, UpstreamError
from .services import ipapi_client, ipify_client
from .validators import IPAddress, ensure_public, parse_ip

bp = Blueprint("main", __name__)


def _discover_addresses() -> dict:
    """Detect this machine's public IPv4/IPv6. Fails only if both are missing."""
    cfg = current_app.config
    ipv4, failure = None, None
    try:
        ipv4 = ipify_client.get_ipv4(cfg["IPIFY_V4_URL"], cfg["HTTP_TIMEOUT"])
    except UpstreamError as exc:
        failure = exc
    ipv6 = ipify_client.get_ipv6(cfg["IPIFY_V6_URL"], cfg["HTTP_TIMEOUT"])
    if ipv4 is None and ipv6 is None:
        raise failure or UpstreamError("Could not detect a public IP address.")
    return {"ipv4": ipv4, "ipv6": ipv6}


def _geolocate(ip_obj: IPAddress) -> dict:
    """Geolocate a public IP, using the SQLite cache when fresh."""
    cfg = current_app.config
    db_path = cfg["DB_PATH"]
    ensure_public(ip_obj)
    ip = str(ip_obj)

    cached = storage.get_cached(db_path, ip, cfg["CACHE_TTL"])
    if cached is not None:
        storage.touch(db_path, ip)
        cached["cached"] = True
        return cached

    result = ipapi_client.lookup(
        ip, cfg["IPAPI_BASE_URL"], cfg["HTTP_TIMEOUT"], cfg["IPAPI_KEY"]
    )
    storage.save(db_path, ip, result)
    return result


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/api/myip")
def myip():
    return jsonify(_discover_addresses())


@bp.get("/api/lookup/me")
def lookup_me():
    addresses = _discover_addresses()
    primary = addresses["ipv4"] or addresses["ipv6"]
    location = _geolocate(parse_ip(primary))
    return jsonify({**addresses, "location": location})


@bp.get("/api/lookup/<ip>")
def lookup_ip(ip: str):
    return jsonify(_geolocate(parse_ip(ip)))


@bp.get("/api/history")
def history():
    raw = request.args.get("limit", "20")
    try:
        limit = int(raw)
    except ValueError:
        raise InvalidParameterError("limit must be an integer.") from None
    if not 1 <= limit <= 100:
        raise InvalidParameterError("limit must be between 1 and 100.")
    return jsonify(storage.recent(current_app.config["DB_PATH"], limit))


@bp.delete("/api/history")
def clear_history():
    storage.clear(current_app.config["DB_PATH"])
    return "", 204
