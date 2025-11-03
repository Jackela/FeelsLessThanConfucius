import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_render_contract_ok(client):
    headers = {"X-API-Key": "test-key"}
    # Minimal valid payload
    payload = {
        "audio_url": "https://example.com/audio/test.wav",
        "timings": [{"start_ms": 0, "end_ms": 100, "unit": "syllable"}],
    }
    resp = client.post("/render", json=payload, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    for k in ("trace_id", "video_url"):
        assert k in data


def test_render_requires_api_key(client):
    resp = client.post(
        "/render", json={"audio_url": "u", "timings": [{"start_ms": 0, "end_ms": 1, "unit": "u"}]}
    )
    assert resp.status_code == 401

