import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def new_trace_id() -> str:
    return uuid.uuid4().hex


@dataclass
class SourceRef:
    passage_id: str
    title: str
    location: str
    confidence: Optional[float] = None


@dataclass
class ProvenanceRecord:
    trace_id: str
    model: str
    prompt_template_version: str
    sources: List[SourceRef] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    latency_ms: Dict[str, int] = field(default_factory=dict)
    confidence: Optional[float] = None


class TraceTimer:
    def __init__(self) -> None:
        self._marks: Dict[str, float] = {}

    def mark(self, name: str) -> None:
        self._marks[name] = time.perf_counter()

    def durations_ms(self) -> Dict[str, int]:
        # Expect marks like: start, text_done, tts_done, render_done
        result: Dict[str, int] = {}
        start = self._marks.get("start", None)
        if start is None:
            return result
        for key in ("text", "tts", "render", "end_to_end"):
            stop_key = {
                "text": "text_done",
                "tts": "tts_done",
                "render": "render_done",
                "end_to_end": "end",
            }[key]
            stop = self._marks.get(stop_key)
            if stop is not None:
                result[key] = int((stop - start) * 1000)
        return result

