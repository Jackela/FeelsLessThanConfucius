from src.api.provenance import new_trace_id


def render_video(audio_url: str, timings: list[dict]) -> dict:
    trace_id = new_trace_id()
    video_url = f"https://example.com/video/{trace_id}.mp4"
    return {"trace_id": trace_id, "video_url": video_url}

