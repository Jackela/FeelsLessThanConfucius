# Research: Confucian RAG Agent (Phase 0)

**Date**: 2025-11-03  
**Branch**: 1-confucian-rag-agent  
**Spec**: D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md

## Decisions

### 1) 语音合成依赖与替代
- Decision: 首选 Edge‑TTS；可替代 ElevenLabs （提供适配器接口）。
- Rationale: Edge‑TTS 延迟稳定、成本低；保留商用替代以容纳风格需求。
- Alternatives: 仅用商用（成本高/锁定）；本地 TTS（部署复杂，音色受限）。

### 2) Live2D 渲染桥接
- Decision: Node Bridge 方案，输入语音节拍（时序）驱动口型，低清晰度输出。
- Rationale: 初期快速落地，满足端到端 p95≤6s 目标。
- Alternatives: 高精度表情捕捉（超出范围）；WebGL 客户端渲染（端能力不确定）。

### 3) 溯源/配额元数据存储
- Decision: 追踪/配额使用轻量 KV/关系型（如 SQLite/轻量 RDB），产出文件走对象存储；向量索引用 FAISS。
- Rationale: 简化运维；满足 30 天保留与配额速率统计。
- Alternatives: 全托管分布式存储（初期超规格）；纯内存（不持久不合规）。

### 4) RAG 评测与抽样
- Decision: 构建含四书问答的离线评测集；每周抽样 100 条线上请求回放评估 Top‑3。
- Rationale: 可操作且成本可控，支撑 ≥85% 目标。
- Alternatives: 大规模自动化评测（初期过重）；仅主观评测（不可量化）。

## Consolidated

- Language/Version: Python 3.11
- Primary Dependencies: FastAPI, LangChain, FAISS, Edge‑TTS/ElevenLabs, Live2D Node Bridge
- Storage: FAISS + 轻量 KV/关系型 + 对象存储
- Testing: pytest
- Target: Linux server
- Project Type: single
- Performance: 文本 p95≤2s；端到端 p95≤6s；Top‑3≥85%
- Constraints: 中文输出；API Key+60 rpm+1000/day；30 天保留；Hybrid 合规
- Scale/Scope: 试点 ≤100 Key，≤50 rps 峰值

