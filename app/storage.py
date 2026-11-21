"""SQLite storage: one row per IP, used as both lookup history and cache."""
import json
import os
import sqlite3
import time
from contextlib import closing
from typing import Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS lookups (
    ip         TEXT PRIMARY KEY,
    payload    TEXT NOT NULL,
    fetched_at REAL NOT NULL,
    last_seen  REAL NOT NULL
)
"""


def _connect(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def init_db(db_path: str) -> None:
    folder = os.path.dirname(db_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(SCHEMA)


def save(db_path: str, ip: str, payload: dict, now: Optional[float] = None) -> None:
    """Insert or refresh the stored lookup for `ip`."""
    ts = time.time() if now is None else now
    with closing(_connect(db_path)) as conn, conn:
        conn.execute(
            "INSERT INTO lookups (ip, payload, fetched_at, last_seen) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(ip) DO UPDATE SET payload = excluded.payload, "
            "fetched_at = excluded.fetched_at, last_seen = excluded.last_seen",
            (ip, json.dumps(payload), ts, ts),
        )


def get_cached(db_path: str, ip: str, ttl: int, now: Optional[float] = None) -> Optional[dict]:
    """Return the stored payload if it is younger than `ttl` seconds, else None."""
    ts = time.time() if now is None else now
    with closing(_connect(db_path)) as conn:
        row = conn.execute(
            "SELECT payload, fetched_at FROM lookups WHERE ip = ?", (ip,)
        ).fetchone()
    if row is None or ts - row[1] > ttl:
        return None
    return json.loads(row[0])


def touch(db_path: str, ip: str, now: Optional[float] = None) -> None:
    """Mark `ip` as just viewed so it moves to the top of the history."""
    ts = time.time() if now is None else now
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("UPDATE lookups SET last_seen = ? WHERE ip = ?", (ts, ip))


def recent(db_path: str, limit: int = 20) -> list[dict]:
    """Most recently viewed lookups, newest first."""
    with closing(_connect(db_path)) as conn:
        rows = conn.execute(
            "SELECT payload FROM lookups ORDER BY last_seen DESC, rowid DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [json.loads(r[0]) for r in rows]


def clear(db_path: str) -> None:
    with closing(_connect(db_path)) as conn, conn:
        conn.execute("DELETE FROM lookups")
