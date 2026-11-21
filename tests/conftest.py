import pytest

from app import create_app

SAMPLE_IPAPI = {
    "ip": "8.8.8.8",
    "version": "IPv4",
    "city": "Mountain View",
    "region": "California",
    "region_code": "CA",
    "country": "US",
    "country_name": "United States",
    "country_code": "US",
    "postal": "94035",
    "latitude": 37.386,
    "longitude": -122.0838,
    "timezone": "America/Los_Angeles",
    "org": "GOOGLE",
    "asn": "AS15169",
}


@pytest.fixture
def sample_ipapi():
    return dict(SAMPLE_IPAPI)


@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "DB_PATH": str(tmp_path / "test.db")})


@pytest.fixture
def client(app):
    return app.test_client()
