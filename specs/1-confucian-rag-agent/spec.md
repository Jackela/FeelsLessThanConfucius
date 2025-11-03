# Feature Specification: Confucian RAG Agent

**Feature Branch**: `[1-confucian-rag-agent]`  
**Created**: 2025-11-03  
**Status**: Draft  
**Input**: User description: "Scope: 构建一个以中文为主要交互语言、基于 RAG（检索增强生成）与 LLM 的“孔孟之道体”数字人系统，整合 TTS（文字转语音）与 Live2D 动画输出，形成低清晰度（low-definition）的 agentic 数字人格，用于自动生成讽喻性短视频与文本。系统范围包括四书语料检索（《论语》《孟子》《大学》《中庸》）、RAG 检索召回与语义匹配、三段式模版文本生成（古意起句→当代转译→固定收尾“——不如孔孟之道”）、TTS 合成语音、Live2D 模型驱动动画、API 接口服务（/generate /speak /render）、内容安全过滤、日志与延迟监控。工程治理遵循 DDD（领域驱动设计）、TDD（测试驱动开发）、DbC（契约式设计）与清洁代码原则，每次改动同步更新 AGENTS.md。输出仅中文但 LLM 可处理混合语料。范围外不包含高精度表情捕捉、实时连麦或大规模微调。性能约束：文本响应 P95≤2s、端到端生成延迟≤6s、RAG Top-3 命中率≥85%、生成内容可追溯至原典出处。"

## Clarifications

### Session 2025-11-03

- Q: API auth and rate limits for /generate, /speak, /render, and provenance endpoints → A: API key per client with per-key rate limits and quotas
- Q: Retention period for logs/provenance tied to trace IDs → A: 30 days
- Q: Baseline per‑key rate limits (per minute) for write endpoints → A: 60 rpm
- Q: Baseline daily quota per key (all write endpoints combined) → A: 1000 requests/day

## User Scenarios & Testing (mandatory)

### User Story 1 - 生成“孔孟之道体”文本 (Priority: P1)

用户基于一个当代主题或素材，获得三段式的中文讽喻文本：古意起句 → 当代转译 → 固定收尾“——不如孔孟之道”。文本附带出处溯源与合规状态。

**Why this priority**: 核心价值在于文本讽喻输出的及时性与风格稳定性。

**Independent Test**: 仅请求文本生成即可完整交付价值（无需语音或视频）。

**Acceptance Scenarios**:

1. Given 用户输入“内卷职场”，When 请求文本生成，Then 返回三段式文本且为中文，并包含至少一条四书出处引用与唯一追踪ID。
2. Given 用户输入“极端言论”，When 请求文本生成，Then 系统返回合规拦截/替代输出，并附带合规状态与原因。

---

### User Story 2 - 生成讽喻短视频 (Priority: P2)

用户从已有三段式文本生成语音并驱动低清晰度动画，获得可分享的短视频。

**Why this priority**: 视频输出提升传播与记忆度，但不阻塞文本 MVP。

**Independent Test**: 给定现成文本，可独立完成语音合成与动画渲染并产出视频。

**Acceptance Scenarios**:

1. Given 已有合规文本，When 请求语音合成，Then 返回中文语音与时间戳节拍用于口型驱动。
2. Given 语音与节拍，When 请求渲染，Then 产出低清晰度动画短视频，端到端生成时间满足约束。

---

### User Story 3 - 溯源与合规查看 (Priority: P2)

用户或审核者查看任一生成结果的出处溯源、检索命中率、合规过滤结果与延迟记录。

**Why this priority**: 透明性与可追溯性是信任与持续优化的基础。

**Independent Test**: 在不生成新内容的前提下，仅查看/导出溯源与合规报告即能独立验收。

**Acceptance Scenarios**:

1. Given 追踪ID，When 查看详情，Then 显示原典出处（书名、篇章、行/段信息）、检索Top-3命中、生成参数与时间线。
2. Given 合规疑虑，When 导出报告，Then 提供可审计的合规与延迟摘要，不含敏感身份信息。
3. Given 缺失或无效API Key，When 访问任何受保护端点（含溯源），Then 返回401；若超出配额或速率（写端点基线60 rpm），Then 返回429并包含重试提示。
4. Given 追踪ID超过保留期，When 查看详情，Then 返回“记录已过期/不可用”的明确说明。
5. Given 单Key当日累计超过配额，When 再次访问写端点，Then 返回429并包含配额重置时间信息。
6. Given 触发合规过滤为高风险，When 请求文本生成，Then 返回拒绝与原因说明；Given 触发为低/中风险，Then 返回替代安全改写文本并标注调整原因。`r`n
### Edge Cases

- 输入为空或过长（截断/提示重试）。
- 语义过于抽象导致低检索召回（提供澄清建议）。
- 没有合适原典（返回“无可靠出处”的替代文本或引导重试）。
- 触发合规规则（输出替代文本与原因，而非原始生成）。
- 缺失或无效API Key（返回401）。
- 速率限制或配额超限（返回429并提示重试/等待）。
- 达到每日配额上限（返回429并指明重置时间）。
- 合规高风险直接拒绝；低/中风险返回替代安全改写（并标注原因）。`r`n
## Requirements (mandatory)

### Functional Requirements

- FR-001: 系统必须接受中文为主的输入并仅输出中文文本；可容忍混合语料输入。
- FR-002: 每次文本输出必须由三段组成：古意起句、当代转译、固定收尾“——不如孔孟之道”。
- FR-003: 每次输出必须包含可审计的溯源信息（书名、篇章、行/段、片段ID、检索Top-K得分、置信度）。
- FR-004: 必须提供内容合规过滤，返回“通过/替代/拒绝”与原因，不泄露身份或隐私。
- FR-005: 必须支持仅文本生成的独立流程（不依赖语音/视频）。
- FR-006: 必须支持在已有文本基础上生成中文语音，并返回语音节拍/时间戳以驱动口型。
- FR-007: 必须支持利用语音与节拍生成低清晰度动画短视频，可供下载或分享。
- FR-008: 必须为每次请求生成唯一追踪ID，并记录端到端时间线（检索→生成→合规→合成/渲染）。
- FR-009: 必须提供可视化或可导出的溯源/合规/延迟报告视图。
- FR-010: 性能：文本响应P95 ≤ 2s；端到端（文本→语音→渲染）P95 ≤ 6s。
- FR-011: 检索效果：RAG Top-3命中率 ≥ 85%（基于内置评测集与周期性抽样）。
- FR-012: 可追溯性：所有文本均可追溯到原典出处；若无可靠出处，须标注并避免伪造引用。
- FR-013: 安全与访问控制：/generate、/speak、/render 以及溯源相关端点必须使用“每客户端API Key”，并实施按Key的速率限制与配额；缺失/无效Key返回401；超限返回429。
- FR-014: 日志与溯源保留：与追踪ID关联的日志/溯源数据至少保留30天，包含生成参数、来源引用与延迟度量；避免记录可识别个人信息；到期后不可再检索（按策略清理）。
- FR-015: 速率限制（写端点）：/generate、/speak、/render 的基线为每Key 60 次/分钟（60 rpm）；达到上限返回429，并提供 Retry-After/配额相关响应头以便客户端退避。
- FR-016: 每日配额：所有写端点合计基线为每Key 1000 次/日；超过配额返回429，并包含配额重置时间（如 UTC 日界重置）与剩余额度信息。
- FR-017: 合规默认策略（Hybrid）：当合规过滤判定为低/中风险时，提供替代安全改写并标注调整原因；当判定为高风险时，直接拒绝并返回拒绝原因；所有判定与处理动作需记录在合规报告中。`r`n
### Key Entities (include if feature involves data)

- Query：用户输入主题或素材的抽象。
- Passage：原典片段，含书名、篇章、行/段、片段ID与内容摘要。
- RetrievalSet：一次检索的Top-K结果与得分。
- SatireText：三段式生成文本及其元数据（语言=中文、风格标签）。
- VoiceTiming：语音片段与节拍时间线。
- RenderJob：动画渲染任务与产出链接。
- Provenance：溯源记录（来源、版本、对齐方式、置信度、追踪ID）。
- SafetyReport：合规过滤结果及原因分类。

## Success Criteria (mandatory)

### Measurable Outcomes

- SC-001: 95% 的文本请求在 2 秒内返回三段式中文文本。
- SC-002: 90% 的从文本到短视频流程在 6 秒内完成产出。
- SC-003: RAG Top-3 命中率 ≥ 85%，并按周出具评测报告与样例。
- SC-004: 100% 的生成结果包含可审计的溯源信息与唯一追踪ID。
- SC-005: 100% 的不合规输入/输出给出替代文本或拒绝，并包含原因说明。
- SC-006: 100% 的生成事件在30天内可检索溯源记录；超过30天后不再可用（符合保留策略）。
- SC-007: 100% 触发合规的请求按Hybrid策略分类与响应，含清晰的“替代/拒绝”标签与原因。`r`n
### Global SLA Alignment (project-wide)

如适用于本特性，需说明如何满足/度量：
- 文本响应时间 < 2 s (p95)
- 端到端（文本→语音→渲染）< 6 s (p95)
- 合规/透明性门槛（溯源日志、合规模型/规则、可审计性）

## Quality Gates (Engineering Integrity)

- TDD：在实现前为每个用户故事编写失败测试，遵循 red→green→refactor。
- DbC：为关键契约定义前置/后置条件与不变式，并以断言或校验体现。
- DDD：标注本特性影响的领域与边界，保持语义一致与聚合清晰。







