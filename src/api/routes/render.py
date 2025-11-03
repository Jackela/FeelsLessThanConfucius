from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="", tags=["render"])


from ..schemas import RenderRequest, RenderResponse
from ...live2d.render import render_video


@router.post("/render", response_model=RenderResponse)
def render_endpoint(payload: RenderRequest):
    if not payload.timings or payload.timings[0].end_ms < payload.timings[0].start_ms:
        raise HTTPException(status_code=400, detail="Invalid timings")
    result = render_video(payload.audio_url, [t.model_dump() for t in payload.timings])
    return RenderResponse(**result)
