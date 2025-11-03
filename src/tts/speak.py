from typing import List, Dict

from src.api.provenance import new_trace_id


def speak_with_timings(text: str) -> Dict:
    """Scaffold TTS: returns a fake audio URL and coarse timings."""
    # Split by ~3 chunks for demo
    chunks = max(1, min(3, len(text) // 4))
    step = max(1, len(text) // chunks)
    timings: List[Dict] = []
    cur = 0
    start = 0
    while cur < len(text):
        end = min(len(text), cur + step)
        timings.append({"start_ms": start, "end_ms": start + 500, "unit": "syllable"})
        start += 500
        cur = end
    trace_id = new_trace_id()
    audio_url = f"https://example.com/audio/{trace_id}.wav"
    return {"trace_id": trace_id, "audio_url": audio_url, "timings": timings}

