import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_generate_contract_ok(client):
    headers = {"X-API-Key": "test-key"}
    resp = client.post("/generate", json={"prompt": "内卷职场"}, headers=headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()

    # Top-level fields
    for k in ("trace_id", "part1_ancient", "part2_modern", "part3_closure", "provenance", "safety", "confidence"):
        assert k in data, f"missing field: {k}"

    # Closure must be the fixed line
    assert data["part3_closure"].endswith("——不如孔孟之道")

    # Provenance schema
    prov = data["provenance"]
    for k in ("trace_id", "model", "prompt_template_version", "sources", "params", "latency_ms", "confidence"):
        assert k in prov, f"missing provenance field: {k}"
    assert isinstance(prov["sources"], list) and len(prov["sources"]) >= 1
    src0 = prov["sources"][0]
    for k in ("passage_id", "title", "location", "confidence"):
        assert k in src0

    # Safety schema
    saf = data["safety"]
    for k in ("risk", "action", "reason"):
        assert k in saf


def test_generate_requires_api_key(client):
    resp = client.post("/generate", json={"prompt": "示例"})
    assert resp.status_code == 401

