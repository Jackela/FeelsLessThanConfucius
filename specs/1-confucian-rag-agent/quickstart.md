# Quickstart: Confucian RAG Agent

This guide shows how to use the main flows with API keys, provenance, and safety policies.

## Prerequisites

- Obtain an API key (header `X-API-Key`).
- Respect limits: 60 rpm per key (write), 1000/day total.

## 1) Generate Confucian-style text

Request (POST `/generate`):

- Inputs: `prompt` (Chinese topic or material)
- Output: `part1_ancient`, `part2_modern`, `part3_closure`, `trace_id`, `provenance`, `safety`
- Safety: high-risk → reject; low/medium → safe rewrite with reason

Example (JSON):

```
curl -s -H "X-API-Key: test" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"内卷职场"}' \
  http://localhost:8000/generate | jq .
```

Streaming (SSE) variant:

```
curl -s -H "X-API-Key: test" \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"内卷职场"}' \
  "http://localhost:8000/generate?stream=true"
```

## 2) Synthesize speech

Request (POST `/speak`):

- Inputs: `text` from step 1
- Output: `audio_url`, `timings` (for lip-sync)

## 3) Render low-definition Live2D video

Request (POST `/render`):

- Inputs: `audio_url`, `timings`
- Output: `video_url`

## 4) View provenance and latency

Request (GET `/provenance/{trace_id}`):

- Shows sources (Four Books references), template version, parameters, and latency timeline
- Records kept for 30 days; after that, responses return “expired/unavailable”

## Errors and limits

- Missing/invalid key → 401
- Rate limit exceeded → 429 (use `Retry-After` header)
- Daily quota exceeded → 429 (includes reset-time info)

## Notes

- Output is Chinese-only; input may be mixed-language.
- Content must remain cultural satire; no identity-based attacks or polarization.
