---

description: "Task list for Confucian RAG Agent"
---

# Tasks: Confucian RAG Agent

**Input**: Design documents from `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with FastAPI in `D:\Code\FeelsLessThanConfucius\src\api\app.py`
- [X] T003 [P] Configure linting/formatting (black/isort/flake8) in `D:\Code\FeelsLessThanConfucius\pyproject.toml`
- [X] T004 Configure CI/CD (GitHub Actions) per constitution gates in `D:\Code\FeelsLessThanConfucius\.github\workflows\ci.yml`
- [X] T005 Add MIT LICENSE and repository policies in `D:\Code\FeelsLessThanConfucius\LICENSE`
- [X] T006 Create/Update AGENTS.md with TDD/DbC/DDD rules in `D:\Code\FeelsLessThanConfucius\AGENTS.md`
- [X] T007 [P] Scaffold API package with routers in `D:\Code\FeelsLessThanConfucius\src\api\routes\__init__.py`
- [X] T008 [P] Add OpenAPI doc sync script placeholder in `D:\Code\FeelsLessThanConfucius\scripts\sync-openapi.ps1`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T009 Setup vector index load/build utilities in `D:\Code\FeelsLessThanConfucius\src\rag\index.py`
- [X] T010 [P] Implement provenance/trace utilities in `D:\Code\FeelsLessThanConfucius\src\api\provenance.py`
- [X] T011 [P] Implement API key auth middleware in `D:\Code\FeelsLessThanConfucius\src\api\middleware\auth.py`
- [X] T012 [P] Implement rate limiting & daily quotas in `D:\Code\FeelsLessThanConfucius\src\api\middleware\ratelimit.py`
- [X] T013 Implement safety filter (Hybrid policy) in `D:\Code\FeelsLessThanConfucius\src\api\safety.py`
- [X] T014 [P] Add observability (structured logs/metrics) in `D:\Code\FeelsLessThanConfucius\src\api\observability.py`

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 生成“孔孟之道体”文本 (Priority: P1) 🎯 MVP

**Goal**: 输入当代主题生成三段式中文文本，附溯源与合规状态

**Independent Test**: 仅调用 `/generate` 即可完整交付（无语音/渲染依赖）

### Tests for User Story 1 (TDD)

- [X] T016 [P] [US1] Contract test for POST /generate in `D:\Code\FeelsLessThanConfucius\tests\contract\test_generate.py`
- [X] T017 [P] [US1] Integration test: text parts + provenance + safety in `D:\Code\FeelsLessThanConfucius\tests\integration\test_generate_flow.py`

### Implementation for User Story 1

- [X] T018 [P] [US1] Define API schemas (Query/SatireText/Provenance/Safety) in `D:\Code\FeelsLessThanConfucius\src\api\schemas.py`
- [X] T019 [P] [US1] Implement retrieval function in `D:\Code\FeelsLessThanConfucius\src\rag\query.py`
- [X] T020 [P] [US1] Implement three-part template generator in `D:\Code\FeelsLessThanConfucius\src\llm\generate.py`
- [X] T021 [US1] Implement route handler for /generate in `D:\Code\FeelsLessThanConfucius\src\api\routes\generate.py`
- [X] T022 [US1] Integrate safety (Hybrid) into generate flow in `D:\Code\FeelsLessThanConfucius\src\api\routes\generate.py`
- [X] T023 [US1] Add trace/provenance logging for generate in `D:\Code\FeelsLessThanConfucius\src\api\routes\generate.py`
- [X] T024 [US1] Update spec and AGENTS.md per implementation in `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md`

- [X] T044 [US1] Include overall and per-source confidence in /generate response in `D:\Code\FeelsLessThanConfucius\src\api\routes\generate.py`
- [X] T045 [P] [US1] Log and persist confidence fields in `D:\Code\FeelsLessThanConfucius\src\api\provenance.py`
- [X] T046 [P] [US1] Add retrieval cache in `D:\Code\FeelsLessThanConfucius\src\rag\cache.py` and wire in `D:\Code\FeelsLessThanConfucius\src\rag\query.py`
- [X] T047 [US1] Add token streaming for /generate in `D:\Code\FeelsLessThanConfucius\src\api\routes\generate.py`

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 生成讽喻短视频 (Priority: P2)

**Goal**: 基于现有文本合成中文语音并驱动低清晰度动画短视频

**Independent Test**: 给定现成文本，可独立完成语音合成与渲染并产出视频

### Tests for User Story 2 (TDD)

- [X] T025 [P] [US2] Contract test for POST /speak in `D:\Code\FeelsLessThanConfucius\tests\contract\test_speak.py`
- [X] T026 [P] [US2] Contract test for POST /render in `D:\Code\FeelsLessThanConfucius\tests\contract\test_render.py`
- [X] T027 [P] [US2] Integration test: text→speech→render E2E in `D:\Code\FeelsLessThanConfucius\tests\integration\test_video_flow.py`

### Implementation for User Story 2

- [X] T028 [P] [US2] Implement TTS with timings in `D:\Code\FeelsLessThanConfucius\src\tts\speak.py`
- [X] T029 [P] [US2] Implement Live2D renderer in `D:\Code\FeelsLessThanConfucius\src\live2d\render.py`
- [X] T030 [US2] Implement routes /speak and /render in `D:\Code\FeelsLessThanConfucius\src\api\routes\speak.py` and `D:\Code\FeelsLessThanConfucius\src\api\routes\render.py`
- [X] T031 [US2] Implement RenderJob tracking in `D:\Code\FeelsLessThanConfucius\src\api\render_job.py`
- [X] T032 [US2] Add error handling and quota headers in `D:\Code\FeelsLessThanConfucius\src\api\routes\render.py`

- [X] T048 [P] [US2] Pre-warm TTS voices at startup in `D:\Code\FeelsLessThanConfucius\src\tts\startup.py` and hook from app init in `D:\Code\FeelsLessThanConfucius\src\api\app.py`
- [X] T049 [US2] Update spec and AGENTS.md per US2 changes in `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 溯源与合规查看 (Priority: P2)

**Goal**: 查看生成结果的溯源/检索命中/合规与延迟，并处理过期记录

**Independent Test**: 仅调用 `/provenance/{trace_id}` 即可验收（无生成依赖）

### Tests for User Story 3 (TDD)

- [X] T033 [P] [US3] Contract test for GET /provenance/{trace_id} in `D:\Code\FeelsLessThanConfucius\tests\contract\test_provenance.py`
- [X] T034 [P] [US3] Integration test: audit view + 30天过期 in `D:\Code\FeelsLessThanConfucius\tests\integration\test_provenance_view.py`

### Implementation for User Story 3

- [X] T035 [P] [US3] Implement provenance service in `D:\Code\FeelsLessThanConfucius\src\api\provenance_service.py`
- [X] T036 [US3] Implement route /provenance/{trace_id} in `D:\Code\FeelsLessThanConfucius\src\api\routes\provenance.py`
- [X] T037 [US3] Implement retention cleanup job in `D:\Code\FeelsLessThanConfucius\src\api\retention.py`
- [X] T038 [US3] Implement exportable audit report in `D:\Code\FeelsLessThanConfucius\src\api\reporting.py`

- [X] T050 [US3] Update spec and AGENTS.md per US3 changes in `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 [P] Documentation updates in `D:\Code\FeelsLessThanConfucius\docs\`
- [ ] T040 Performance tuning across modules in `D:\Code\FeelsLessThanConfucius\src\`
- [ ] T041 [P] Add red‑team safety tests in `D:\Code\FeelsLessThanConfucius\tests\integration\test_safety_hybrid.py`
- [ ] T042 [P] Latency verification scripts in `D:\Code\FeelsLessThanConfucius\scripts\latency_check.py`
- [ ] T043 OpenAPI docs review/sync in `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\contracts\openapi.yaml`

- [X] T051 [P] Add cache/stream/pre-warm impact checks in `D:\Code\FeelsLessThanConfucius\scripts\latency_check.py`
- [X] T052 Create offline RAG eval set in `D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\eval\README.md`
- [X] T053 [P] Implement weekly sampling & replay in `D:\Code\FeelsLessThanConfucius\scripts\rag_eval.py`
- [X] T054 Schedule weekly CI job in `D:\Code\FeelsLessThanConfucius\.github\workflows\rag-eval.yml`
- [X] T055 Publish weekly report in `D:\Code\FeelsLessThanConfucius\docs\rag-eval\index.md`
- [X] T056 Create ARCHITECTURE.md in `D:\Code\FeelsLessThanConfucius\ARCHITECTURE.md`
- [X] T057 Create ROADMAP.md in `D:\Code\FeelsLessThanConfucius\ROADMAP.md`
- [X] T058 Create confucius_prompt.spec.md in `D:\Code\FeelsLessThanConfucius\specs\confucius_prompt.spec.md`
- [X] T059 Create rag_pipeline.spec.md in `D:\Code\FeelsLessThanConfucius\specs\rag_pipeline.spec.md`
- [X] T060 Create metrics dashboard doc in `D:\Code\FeelsLessThanConfucius\docs\observability.md`
- [X] T061 [P] Implement provenance export pipeline in `D:\Code\FeelsLessThanConfucius\scripts\export_provenance.py`
- [X] T062 Add SLA alerts workflow in `D:\Code\FeelsLessThanConfucius\.github\workflows\alerts.yml`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): No dependencies
- Foundational (Phase 2): Depends on Setup — BLOCKS all user stories
- User Stories (Phase 3+): Start after Foundational; US1/US2/US3 can proceed in parallel
- Polish (Final Phase): Depends on desired stories being complete

### User Story Dependencies

- User Story 1 (P1): Independent after Foundational
- User Story 2 (P2): Independent after Foundational（可使用现成文本）
- User Story 3 (P2): Independent after Foundational（只读视图）

### Within Each User Story

- Tests (TDD) MUST fail first, then implement
- Models/schemas → services → routes → integration
- Story complete before moving to next priority

### Parallel Opportunities

- Setup tasks T003/T007/T008 can run in parallel
- Foundational tasks T010/T011/T012/T014 can run in parallel
- US1 tests T016/T017 can run in parallel；US2 tests T025–T027；US3 tests T033–T034
- US2 T028/T029 parallel; US3 T035 parallel to US2 work

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup + Foundational
2. Implement US1 generate flow (+ tests)
3. Validate and demo

### Incremental Delivery

1. Add US2 (speech+render) → test independently → demo
2. Add US3 (provenance view) → test independently → demo









