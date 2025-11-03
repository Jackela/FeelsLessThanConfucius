import logging
import time
from typing import Callable

from starlette.requests import Request


logger = logging.getLogger("confucian_rag_agent")
logging.basicConfig(level=logging.INFO)


async def log_request_timing(request: Request, call_next: Callable):
    start = time.perf_counter()
    response = await call_next(request)
    dur_ms = int((time.perf_counter() - start) * 1000)
    logger.info(
        "path=%s status=%s duration_ms=%s", request.url.path, response.status_code, dur_ms
    )
    return response

