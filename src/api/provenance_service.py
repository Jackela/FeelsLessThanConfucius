from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from .db import get_conn


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_provenance(trace_id: str, data: Dict[str, Any]) -> None:
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO provenance(trace_id, data, created_at) VALUES (?, ?, ?)",
        (trace_id, json.dumps(data, ensure_ascii=False), _now_iso()),
    )
    conn.commit()


def get_provenance(trace_id: str, retention_days: int = 30) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.execute(
        "SELECT data, created_at FROM provenance WHERE trace_id = ?", (trace_id,)
    )
    row = cur.fetchone()
    if not row:
        return None
    data_json, created_at = row
    try:
        created_dt = datetime.fromisoformat(created_at)
    except Exception:
        created_dt = datetime.now(timezone.utc)
    if created_dt < datetime.now(timezone.utc) - timedelta(days=retention_days):
        return None
    return json.loads(data_json)


def cleanup_retention(retention_days: int = 30) -> int:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()
    conn = get_conn()
    cur = conn.execute("DELETE FROM provenance WHERE created_at < ?", (cutoff,))
    conn.commit()
    return cur.rowcount
