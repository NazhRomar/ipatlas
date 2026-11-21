import pytest

from app import storage


@pytest.fixture
def db(tmp_path):
    path = str(tmp_path / "s.db")
    storage.init_db(path)
    return path


def test_t13_cache_hit_within_ttl(db):
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8"}, now=1000)
    assert storage.get_cached(db, "8.8.8.8", ttl=60, now=1030) == {"ip": "8.8.8.8"}


def test_t14_cache_miss_after_ttl(db):
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8"}, now=1000)
    assert storage.get_cached(db, "8.8.8.8", ttl=60, now=1061) is None


def test_cache_miss_unknown_ip(db):
    assert storage.get_cached(db, "1.1.1.1", ttl=60) is None


def test_t15_recent_newest_first(db):
    storage.save(db, "1.1.1.1", {"ip": "1.1.1.1"}, now=1)
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8"}, now=2)
    storage.save(db, "9.9.9.9", {"ip": "9.9.9.9"}, now=3)
    assert [r["ip"] for r in storage.recent(db, 10)] == ["9.9.9.9", "8.8.8.8", "1.1.1.1"]
    assert len(storage.recent(db, 2)) == 2


def test_touch_moves_entry_to_top(db):
    storage.save(db, "1.1.1.1", {"ip": "1.1.1.1"}, now=1)
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8"}, now=2)
    storage.touch(db, "1.1.1.1", now=3)
    assert storage.recent(db, 10)[0]["ip"] == "1.1.1.1"


def test_save_same_ip_updates_not_duplicates(db):
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8", "city": "A"}, now=1)
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8", "city": "B"}, now=2)
    rows = storage.recent(db, 10)
    assert len(rows) == 1 and rows[0]["city"] == "B"


def test_clear(db):
    storage.save(db, "8.8.8.8", {"ip": "8.8.8.8"})
    storage.clear(db)
    assert storage.recent(db, 10) == []


def test_sql_injection_string_is_just_data(db):
    evil = "8.8.8.8'; DROP TABLE lookups;--"
    storage.save(db, evil, {"ip": evil})
    assert storage.get_cached(db, evil, ttl=60) == {"ip": evil}
    assert len(storage.recent(db, 10)) == 1
