import os
import sqlite3
from pathlib import Path
from typing import Optional


DB_PATH = Path(os.getcwd()) / "data" / "app.db"
_conn: Optional[sqlite3.Connection] = None


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS provenance (
            trace_id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quota_minute (
            api_key TEXT NOT NULL,
            minute_bucket INTEGER NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (api_key, minute_bucket)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quota_daily (
            api_key TEXT NOT NULL,
            day_bucket TEXT NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (api_key, day_bucket)
        )
        """
    )
    conn.commit()


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH.as_posix(), check_same_thread=False)
    return _conn
