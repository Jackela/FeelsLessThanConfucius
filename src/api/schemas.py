from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="当代主题或素材")


class SourceRef(BaseModel):
    passage_id: str
    title: str
    location: str
    confidence: Optional[float] = None


class Provenance(BaseModel):
    trace_id: str
    model: str
    prompt_template_version: str
    sources: List[SourceRef]
    params: Dict[str, Any]
    latency_ms: Dict[str, int]
    confidence: Optional[float] = None


class Safety(BaseModel):
    risk: str
    action: str
    reason: str


class GenerateResponse(BaseModel):
    trace_id: str
    part1_ancient: str
    part2_modern: str
    part3_closure: str
    confidence: float
    provenance: Provenance
    safety: Safety


class SpeakRequest(BaseModel):
    text: str


class SpeakTiming(BaseModel):
    start_ms: int
    end_ms: int
    unit: str


class SpeakResponse(BaseModel):
    trace_id: str
    audio_url: str
    timings: list[SpeakTiming]


class RenderRequest(BaseModel):
    audio_url: str
    timings: list[SpeakTiming]


class RenderResponse(BaseModel):
    trace_id: str
    video_url: str
