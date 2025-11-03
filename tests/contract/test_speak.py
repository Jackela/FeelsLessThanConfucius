import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_speak_contract_ok(client):
    headers = {"X-API-Key": "test-key"}
    resp = client.post("/speak", json={"text": "当代摸鱼不如读书"}, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    for k in ("trace_id", "audio_url", "timings"):
        assert k in data
    assert isinstance(data["timings"], list) and len(data["timings"]) >= 1
    t0 = data["timings"][0]
    for k in ("start_ms", "end_ms", "unit"):
        assert k in t0


def test_speak_requires_api_key(client):
    resp = client.post("/speak", json={"text": "示例"})
    assert resp.status_code == 401

