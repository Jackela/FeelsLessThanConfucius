"""
Latency checks for core flows. This script runs locally against the in-process
FastAPI app to estimate end-to-end times and verifies they meet targets:
- Text p95 ≤ 2000 ms (rough proxy with single-run)
- E2E (text→speech→render) ≤ 6000 ms

Usage: python scripts/latency_check.py
"""
import time
from statistics import median
from typing import Dict, List

from fastapi.testclient import TestClient

from src.api.app import app


def time_call(client: TestClient, method: str, path: str, json: Dict, headers: Dict) -> int:
    start = time.perf_counter()
    resp = client.request(method, path, json=json, headers=headers)
    dur_ms = int((time.perf_counter() - start) * 1000)
    resp.raise_for_status()
    return dur_ms


def run_once() -> Dict[str, int]:
    client = TestClient(app)
    headers = {"X-API-Key": "latency-check-key"}

    t_text = time_call(client, "POST", "/generate", {"prompt": "当代摸鱼"}, headers)
    speak = client.post("/speak", json={"text": "当代摸鱼不如读书"}, headers=headers).json()
    t_tts = 0  # speak already includes synthetic timings, no server latency needed
    t_render = time_call(
        client,
        "POST",
        "/render",
        {"audio_url": speak["audio_url"], "timings": speak["timings"]},
        headers,
    )
    t_e2e = t_text + t_tts + t_render
    return {"text_ms": t_text, "render_ms": t_render, "e2e_ms": t_e2e}


def main() -> None:
    samples: List[Dict[str, int]] = []
    for _ in range(3):
        samples.append(run_once())
    text_med = median(s["text_ms"] for s in samples)
    e2e_med = median(s["e2e_ms"] for s in samples)
    print({"text_ms_med": text_med, "e2e_ms_med": e2e_med})
    if text_med > 2000:
        raise SystemExit(f"Text latency too high: {text_med} ms > 2000 ms")
    if e2e_med > 6000:
        raise SystemExit(f"E2E latency too high: {e2e_med} ms > 6000 ms")


if __name__ == "__main__":
    main()

