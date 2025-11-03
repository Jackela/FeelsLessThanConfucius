# Observability

## Signals

- Structured request timing logs (path, status, duration_ms)
- Provenance exports (JSONL): trace_id, model, template, sources, latency_ms, confidence
- SLA checks: scripts/latency_check.py in CI, alerts workflow

## Dashboards

- Latency distributions (text, end_to_end)
- Error rates (4xx/5xx)
- Rate-limit/Quota events (429)

