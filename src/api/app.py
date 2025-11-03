from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import generate, speak, render, provenance
from .middleware.auth import APIKeyMiddleware
from .middleware.ratelimit import RateLimitMiddleware
from ..tts.startup import prewarm as tts_prewarm
from .observability import log_request_timing
from .db import init_db


def create_app() -> FastAPI:
    app = FastAPI(title="Confucian RAG Agent API")

    # Basic CORS (adjust as needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Security middlewares
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(RateLimitMiddleware)

    # Routers (handlers implemented in story phases)
    app.include_router(generate.router)
    app.include_router(speak.router)
    app.include_router(render.router)
    app.include_router(provenance.router)

    # Initialize DB and pre-warm TTS voices
    init_db()
    tts_prewarm()

    # Observability: request timing
    app.middleware("http")(log_request_timing)

    return app


app = create_app()
