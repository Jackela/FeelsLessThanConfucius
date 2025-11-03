import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_provenance_contract_ok(client):
    headers = {"X-API-Key": "k"}
    # First generate to create provenance
    gr = client.post("/generate", json={"prompt": "内卷职场"}, headers=headers)
    assert gr.status_code == 200, gr.text
    trace_id = gr.json()["trace_id"]

    pr = client.get(f"/provenance/{trace_id}", headers=headers)
    assert pr.status_code == 200, pr.text
    data = pr.json()
    for k in ("trace_id", "model", "prompt_template_version", "sources", "params", "latency_ms", "confidence"):
        assert k in data

