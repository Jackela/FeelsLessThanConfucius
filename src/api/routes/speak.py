from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="", tags=["speak"])


from ..schemas import SpeakRequest, SpeakResponse
from ...tts.speak import speak_with_timings


@router.post("/speak", response_model=SpeakResponse)
def speak_endpoint(payload: SpeakRequest):
    result = speak_with_timings(payload.text)
    return SpeakResponse(**result)
