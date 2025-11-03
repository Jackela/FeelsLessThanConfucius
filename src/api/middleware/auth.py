from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class APIKeyMiddleware(BaseHTTPMiddleware):
    header_name = "X-API-Key"

    async def dispatch(self, request: Request, call_next) -> Response:
        # Only protect API routes (all our routes are API)
        api_key: Optional[str] = request.headers.get(self.header_name)
        if not api_key:
            return JSONResponse({"detail": "Missing API key"}, status_code=401)

        # TODO: validate api_key against store; scaffold accepts any non-empty key
        return await call_next(request)

