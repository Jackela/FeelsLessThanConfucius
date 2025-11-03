import time
from datetime import datetime, timezone
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from ..ratelimit_store import (
    inc_minute,
    inc_daily,
    seconds_to_next_utc_minute,
    seconds_to_next_utc_midnight,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Per-key rate limiting (60 rpm) and daily quota (1000/day) scaffold.

    In-memory implementation suitable for a single-process scaffold.
    """

    rpm_limit = 60
    daily_limit = 1000

    async def dispatch(self, request: Request, call_next) -> Response:
        # Only apply to write endpoints per spec: /generate, /speak, /render
        path = request.url.path
        if path not in ("/generate", "/speak", "/render"):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key") or ""
        if not api_key:
            return JSONResponse({"detail": "Missing API key"}, status_code=401)

        now = datetime.now(timezone.utc)
        minute_bucket = int(time.time() // 60)
        day_bucket = now.strftime("%Y-%m-%d")

        # Increment counters in durable store
        mcount = inc_minute(api_key, minute_bucket)
        dcount = inc_daily(api_key, day_bucket)

        # Evaluate after increment (simpler scaffold)
        if mcount > self.rpm_limit:
            retry_after = seconds_to_next_utc_minute()
            return JSONResponse(
                {"detail": "Rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )

        if dcount > self.daily_limit:
            retry_after = seconds_to_next_utc_midnight()
            return JSONResponse(
                {"detail": "Daily quota exceeded"},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)
