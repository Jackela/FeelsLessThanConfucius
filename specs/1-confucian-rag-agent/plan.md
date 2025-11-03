# Implementation Plan: Confucian RAG Agent

**Branch**: `[1-confucian-rag-agent]` | **Date**: 2025-11-03 | **Spec**: D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md
**Input**: Feature specification from `/specs/1-confucian-rag-agent/spec.md`

## Summary

面向中文输出的“孔孟之道体”数字人：以四书为知识源通过 RAG+LLM 生成三段式讽喻文本，并可合成语音和低清晰度 Live2D 短视频。提供溯源与合规报告，满足文本 p95≤2s、端到端 p95≤6s、RAG Top-3≥85%。

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, LangChain, FAISS, Edge‑TTS/ElevenLabs (voice), Live2D Node Bridge  
**Storage**: FAISS 向量索引（本地/持久卷）、对象存储（音视频产出）、轻量 KV/DB 用于配额与追踪  
**Testing**: pytest（单元/契约/集成）  
**Target Platform**: Linux server  
**Project Type**: single  
**Performance Goals**: 文本 p95≤2s；端到端 p95≤6s；Top‑3≥85%  
**Constraints**: 中文输出、Hybrid 合规策略、API Key+60 rpm+1000/day、30 天溯源保留  
**Scale/Scope**: 早期试点（≤100 活跃 Key，≤50 rps 峰值）

## Constitution Check

- Cultural Irony: 仅批评观点/行为；三段式文本；禁止身份攻击（通过合规过滤与模板约束）。
- Technological Transparency: 每次响应记录模型/模板版本、Top‑K 来源、参数、置信度；提供 `/provenance`；追踪ID。
- Module Autonomy: rag/llm/tts/live2d/api 以契约隔离，适配器可替换实现；无隐藏耦合。
- Lightweight First: 以 Prompt+LoRA 为先；缓存/流式；满足 p95 延迟目标。
- Compliance & Safety: 输入/输出多层过滤；文化讽喻范围；Hybrid 策略（替代/拒绝）。
- Engineering Integrity: TDD、DbC、DDD；修改同步 `*.spec.md` 与 `AGENTS.md`；契约先行。

Status: PASS（无需豁免）。

## Project Structure

```text
src/
├── rag/
├── llm/
├── tts/
├── live2d/
└── api/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: 单仓单项目（single），以模块文件夹对应契约与测试目录。

## Complexity Tracking

（当前无违例项）

---

## Phase 0: Outline & Research

Unknowns extracted from Technical Context:
- 依赖实现选型与替代：Edge‑TTS vs ElevenLabs；Live2D 桥接具体方案。
- 存储细节：对象存储与追踪/配额元数据的持久化形式。
- 评测与监控：Top‑3≥85% 的离线评测集与周期性抽样策略。

Research tasks:
- Research 语音合成依赖与替代（Edge‑TTS/ElevenLabs） for Confucian RAG Agent
- Research Live2D 渲染桥接与口型驱动 for Confucian RAG Agent
- Research 溯源/配额元数据存储（KV vs 关系型） for Confucian RAG Agent
- Research RAG Top‑3 评测与周度抽样方案 for Confucian RAG Agent

See D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\research.md for decisions.

---

## Phase 1: Design & Contracts

Deliverables:
- data-model.md：实体、字段、关系、状态机（RenderJob）。
- contracts/openapi.yaml：/generate、/speak、/render、/provenance 端点契约。
- quickstart.md：主要用例调用与合规模式说明。
- Agent context：更新失败（脚本缺失），记录手工步骤。

Post-design Constitution Check: PASS（契约与延迟/安全/溯源均覆盖）。

