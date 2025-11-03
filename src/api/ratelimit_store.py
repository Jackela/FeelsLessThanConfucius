import time
from datetime import datetime, timezone
from typing import Tuple

from .db import get_conn


def inc_minute(api_key: str, minute_bucket: int) -> int:
    conn = get_conn()
    cur = conn.execute(
        "SELECT count FROM quota_minute WHERE api_key = ? AND minute_bucket = ?",
        (api_key, minute_bucket),
    )
    row = cur.fetchone()
    if row:
        cnt = row[0] + 1
        conn.execute(
            "UPDATE quota_minute SET count = ? WHERE api_key = ? AND minute_bucket = ?",
            (cnt, api_key, minute_bucket),
        )
    else:
        cnt = 1
        conn.execute(
            "INSERT INTO quota_minute(api_key, minute_bucket, count) VALUES (?, ?, ?)",
            (api_key, minute_bucket, cnt),
        )
    conn.commit()
    return cnt


def inc_daily(api_key: str, day_bucket: str) -> int:
    conn = get_conn()
    cur = conn.execute(
        "SELECT count FROM quota_daily WHERE api_key = ? AND day_bucket = ?",
        (api_key, day_bucket),
    )
    row = cur.fetchone()
    if row:
        cnt = row[0] + 1
        conn.execute(
            "UPDATE quota_daily SET count = ? WHERE api_key = ? AND day_bucket = ?",
            (cnt, api_key, day_bucket),
        )
    else:
        cnt = 1
        conn.execute(
            "INSERT INTO quota_daily(api_key, day_bucket, count) VALUES (?, ?, ?)",
            (api_key, day_bucket, cnt),
        )
    conn.commit()
    return cnt


def seconds_to_next_utc_minute() -> int:
    now = int(time.time())
    return 60 - (now % 60)


def seconds_to_next_utc_midnight() -> int:
    now = datetime.now(timezone.utc)
    tomorrow = (now.replace(hour=0, minute=0, second=0, microsecond=0)).date().toordinal() + 1
    midnight = datetime.fromordinal(tomorrow).replace(tzinfo=timezone.utc)
    return int((midnight - now).total_seconds())

