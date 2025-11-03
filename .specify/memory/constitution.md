<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles: None (added new principle)
- Added sections:
  - Principle: Engineering Integrity (TDD, DbC, DDD, spec + AGENTS.md sync)
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (added Engineering Integrity gates)
  - ✅ .specify/templates/spec-template.md (added Quality Gates alignment)
  - ✅ .specify/templates/tasks-template.md (added engineering integrity tasks)
  - ✅ AGENTS.md (created with coding discipline rules)
  - ⚠ N/A .specify/templates/commands/*.md (directory not present)
- Deferred TODOs:
  - TODO(RATIFICATION_DATE): Original adoption date unknown; set on first ratification
-->

<!--
Sync Impact Report
- Version change: N/A → 1.0.0
- Modified principles:
  - PRINCIPLE_1_NAME → Cultural Irony (文化反讽)
  - PRINCIPLE_2_NAME → Technological Transparency (技术透明)
  - PRINCIPLE_3_NAME → Module Autonomy (模块自治)
  - PRINCIPLE_4_NAME → Lightweight First (轻量优先)
  - PRINCIPLE_5_NAME → Compliance & Safety (合规安全)
- Added sections: Architecture & Modules; Engineering Standards & SLAs
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Constitution Check gates aligned)
  - ✅ .specify/templates/spec-template.md (SLA alignment note added)
  - ✅ .specify/templates/tasks-template.md (transparency/safety/perf tasks added)
  - ⚠ N/A .specify/templates/commands/*.md (directory not present)
- Deferred TODOs:
  - TODO(RATIFICATION_DATE): Original adoption date unknown; set on first ratification
-->

# Feels Less Than Confucius (感觉不如孔孟之道) Constitution

## Core Principles

### Cultural Irony (文化反讽)
Non‑negotiables:
- Critique ideas, policies, arguments, and behaviors — never identities.
- Strictly prohibit attacks on protected characteristics, harassment, or doxxing.
- Satire MUST anchor in Confucian canon passages retrieved via RAG, with citations.
- Output tone: “孔孟之道体” — witty, respectful, didactic, never demeaning.
Rationale: Keeps discourse focused on cultural critique and learning, avoiding personal harm.

### Technological Transparency (技术透明)
Non‑negotiables:
- Every response MUST log provenance: model name/version, prompt template version,
  top‑k sources (ids, titles, line refs), sampling params, and confidence.
- Expose a `/provenance` endpoint and attach per‑response trace ids for auditability.
- Document data pipelines: corpus scope, preprocessing, embedding model, and updates.
Rationale: Transparent systems are auditable, improvable, and build user trust.

### Module Autonomy (模块自治)
Non‑negotiables:
- RAG, LLM, TTS, and Live2D are independently replaceable via stable contracts.
- No cross‑module hidden coupling: communicate only through API/contracts.
- Provide adapters for at least two implementations per module where feasible.
Rationale: Swapability reduces lock‑in and enables fast experimentation.

### Lightweight First (轻量优先)
Non‑negotiables:
- Prefer Prompt Engineering + LoRA over full fine‑tuning or heavyweight retraining.
- Enforce latency budgets: text < 2 s p95; TTS+Live2D < 1.5 s p95.
- Cache retrievals, stream tokens, and pre‑warm TTS voices; justify any heavy ops.
Rationale: Lower cost, faster iteration, and better user experience.

### Compliance & Safety (合规安全)
Non‑negotiables:
- Prohibit hate speech and political polarization content.
- Apply layered safety: input moderation, RAG source filtering, output moderation.
- Maintain appeal/escalation process and red‑team test set for recurring risks.
Rationale: Ensures legal/ethical compliance and protects users and the project.

### Engineering Integrity
Non‑negotiables:
- Practice Test‑Driven Development (TDD): write failing tests before implementation;
  maintain red‑green‑refactor discipline and adequate coverage for changes.
- Apply Design by Contract (DbC): specify preconditions, postconditions, and
  invariants at module boundaries; enforce via assertions or checks.
- Structure architecture with Domain‑Driven Design (DDD): explicit domain
  boundaries, ubiquitous language, and clear aggregates.
- For every module change, MUST include tests, updated `*.spec.md`, and synchronized
  `AGENTS.md` descriptors in the same commit.
- Refactors MUST preserve functional parity and documentation consistency.
Rationale: Enforces predictable quality, stable contracts, and traceable design decisions.

## Architecture & Modules

- rag: Confucian texts loading and vector retrieval (LangChain/FAISS). Include dataset
  curation, embeddings, chunking, and retrieval configuration with source ids.
- llm: Prompt‑template generation of “孔孟之道体” content (OpenAI GPT‑5). Maintain fixed
  satire templates and parameter presets; version all prompt specs.
- tts: Speech synthesis (Edge‑TTS/ElevenLabs). Provide voice profiles and latency targets.
- live2d: Animation output (Live2D + Node Bridge). Support lip‑sync with TTS timings.
- api: Interface layer (FastAPI/Gradio). Provide JSON/stream endpoints and provenance ids.

Interface Contracts (high‑level):
- rag.query(input: text) → { passages[], citations[], trace_id }
- llm.generate(prompt_spec, context) → { text, trace_id, params }
- tts.speak(text, voice) → { audio_url|bytes, timings }
- live2d.render(audio, timings, avatar) → { video_url|stream }
- api routes expose above with authentication and rate limiting.

## Engineering Standards & SLAs

- Branching: Git Flow (main/dev/feature/*). PRs target `dev`; releases from `main`.
- CI/CD: GitHub Actions — unit/integration tests, lint/format, safety checks,
  provenance schema validation, latency budgets.
- License: MIT.
- Content scope: Cultural satire only — no identity‑based targeting or polarization.
- Core deliverables: ARCHITECTURE.md, ROADMAP.md, confucius_prompt.spec.md,
  rag_pipeline.spec.md, integration test scripts.
- Success metrics (project‑wide):
  - Text response time < 2 s (p95)
  - TTS+Live2D end‑to‑end latency < 1.5 s (p95)
  - User retention > 30%
  - Hot meme response cycle < 12 h
- Observability: Structured logs with trace ids, metrics dashboard, error budgets,
  provenance log export.

## Governance

- Supremacy: This Constitution supersedes other practices for scope it governs.
- Compliance gate: Every PR MUST include a “Constitution Compliance” checklist
  covering the five principles, provenance logging, and SLA impact.
- Amendments: Open a PR labeled `governance` with rationale, redlines, migration
  plan, and expected impact on SLAs. Obtain maintainer approval.
- Versioning policy (semantic):
  - MAJOR: Backward‑incompatible governance/principle removals or redefinitions.
  - MINOR: New principle/section or materially expanded guidance.
  - PATCH: Clarifications, wording, or non‑semantic refinements.
- Reviews: CI MUST verify safety checks, provenance schema, and latency budgets.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown — set on first ratification | **Last Amended**: 2025-11-03
