import json
from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

from .. import safety as safety_mod
from ..provenance import new_trace_id, TraceTimer
from ..schemas import GenerateRequest, GenerateResponse, Provenance as ProvModel, SourceRef
from ...rag.query import retrieve
from ..provenance_service import save_provenance

router = APIRouter(prefix="", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
def generate_text(req: GenerateRequest, stream: bool = False):
    timer = TraceTimer()
    timer.mark("start")
    trace_id = new_trace_id()

    # Retrieval (dummy)
    sources_raw = retrieve(req.prompt, topk=3)

    # Safety decision
    decision = safety_mod.decide_policy(req.prompt)

    # Generate three-part text (scaffold)
    part1 = f"子曰：{req.prompt}，可为世风之一观。"
    modern = f"当下之事，{req.prompt}不过镜中花水中月。"
    closure = "——不如孔孟之道"

    if decision.action == "alter":
        modern = modern.replace("极端", "过激")
    if decision.action == "reject":
        raise HTTPException(status_code=400, detail=decision.reason)

    timer.mark("text_done")
    timer.mark("end")

    prov = ProvModel(
        trace_id=trace_id,
        model="gpt-5",
        prompt_template_version="v1",
        sources=[SourceRef(**s) for s in sources_raw],
        params={"topk": 3},
        latency_ms=timer.durations_ms(),
        confidence=0.9,
    )
    # Persist provenance for later audit view
    save_provenance(trace_id, prov.model_dump())

    if stream:
        def sse() -> bytes:
            # Send parts as separate SSE messages, then metadata
            payloads = [
                {"type": "part1_ancient", "text": part1},
                {"type": "part2_modern", "text": modern},
                {"type": "part3_closure", "text": closure},
            ]
            for p in payloads:
                yield f"event: part\n".encode("utf-8")
                yield f"data: {json.dumps(p, ensure_ascii=False)}\n\n".encode("utf-8")
            meta = {
                "trace_id": trace_id,
                "confidence": 0.9,
                "safety": decision.__dict__,
                "provenance": prov.model_dump(),
            }
            yield f"event: meta\n".encode("utf-8")
            yield f"data: {json.dumps(meta, ensure_ascii=False)}\n\n".encode("utf-8")

        return StreamingResponse(sse(), media_type="text/event-stream")

    return GenerateResponse(
        trace_id=trace_id,
        part1_ancient=part1,
        part2_modern=modern,
        part3_closure=closure,
        confidence=0.9,
        provenance=prov,
        safety=decision.__dict__,
    )
