# ARCHITECTURE: Confucian RAG Agent

## Modules

- `src/rag`: retrieval and caching (later FAISS integration)
- `src/llm`: prompt template + generation (three-part style)
- `src/tts`: speech synthesis and timings (pre-warm)
- `src/live2d`: low-definition animation rendering
- `src/api`: FastAPI app, routes, middleware, provenance, safety, reporting

## Contracts (API)

- POST `/generate` → three-part text + provenance + safety + confidence
- POST `/speak` → audio_url + timings
- POST `/render` → video_url
- GET `/provenance/{trace_id}` → provenance JSON

## Cross-cutting

- Security: API key + rate limit (60 rpm write) + 1000/day
- SLAs: text p95≤2s, E2E p95≤6s
- Retention: provenance 30 days
- Observability: request timing logs, export pipeline, dashboard docs
 - Streaming: `/generate?stream=true` provides SSE events for parts and meta
