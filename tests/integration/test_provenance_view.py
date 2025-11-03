from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from src.api.app import app
from src.api.provenance_service import cleanup_retention


def test_provenance_view_and_expiry():
    client = TestClient(app)
    headers = {"X-API-Key": "k"}

    # Create a fresh provenance via /generate
    gr = client.post("/generate", json={"prompt": "当代摸鱼"}, headers=headers)
    assert gr.status_code == 200
    trace_id = gr.json()["trace_id"]
    ok = client.get(f"/provenance/{trace_id}", headers=headers)
    assert ok.status_code == 200

    # Force expiry by backdating the stored record
    # Emulate expiry by running cleanup with zero-day retention
    cleanup_retention(0)
    expired = client.get(f"/provenance/{trace_id}", headers=headers)
    assert expired.status_code == 404
