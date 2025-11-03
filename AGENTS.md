# AGENTS.md

Scope: Applies to the entire repository (root).

## Engineering Integrity

- TDD: Write failing tests first; follow red→green→refactor.
- DbC: Define/enforce preconditions, postconditions, invariants at module boundaries.
- DDD: Maintain explicit domains, bounded contexts, aggregates, and ubiquitous language.
- Change set discipline: Every module change MUST include tests, updated `*.spec.md`,
  and synchronized updates to this AGENTS.md when coding discipline or architecture
  rules are amended.
- Refactors MUST preserve functional parity and documentation consistency.

## Workflow

- Branching: Git Flow (`main`/`dev`/`feature/*`).
- PRs: Include Constitution Compliance checklist, updated specs, and links to tests.
- Provenance: Ensure `/provenance` exposure and trace ids in API where applicable.

## Contracts & Modules

- rag, llm, tts, live2d modules communicate via explicit contracts only.
- Avoid hidden coupling; prefer adapters to enable swapability.



## API Access & SLAs (Summary)
- API Key per client with per-key rate limits and daily quotas.
- Baselines: 60 rpm write; 1000/day; 30-day provenance retention.
- Performance: Text p95≤2s; E2E p95≤6s.

