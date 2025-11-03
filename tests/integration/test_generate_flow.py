from fastapi.testclient import TestClient

from src.api.app import app


def test_generate_flow_three_parts_and_provenance():
    client = TestClient(app)
    headers = {"X-API-Key": "test-key"}
    r = client.post("/generate", json={"prompt": "当代摸鱼"}, headers=headers)
    assert r.status_code == 200, r.text
    d = r.json()

    # Three parts present and non-empty
    assert d["part1_ancient"] and d["part2_modern"] and d["part3_closure"].endswith("——不如孔孟之道")

    # Provenance present with at least one source and latency metrics
    prov = d["provenance"]
    assert prov["trace_id"] == d["trace_id"]
    assert isinstance(prov["sources"], list) and len(prov["sources"]) >= 1
    assert "end_to_end" in prov["latency_ms"] or "text" in prov["latency_ms"]

    # Safety should be pass/alter for benign input (not reject)
    assert d["safety"]["action"] in ("pass", "alter")

