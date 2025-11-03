# Data Model: Confucian RAG Agent

**Spec**: D:\Code\FeelsLessThanConfucius\specs\1-confucian-rag-agent\spec.md  
**Date**: 2025-11-03

## Entities

- Query
  - id (trace_id, string, unique)
  - text (string, required, zh)
  - created_at (timestamp)

- Passage
  - id (string, unique)
  - source (enum: 论语/孟子/大学/中庸)
  - location (string: 篇章/行段)
  - content (string)

- RetrievalSet
  - id (string)
  - query_id (trace_id)
  - items: [ { passage_id, score } ] (top‑k)

- SatireText
  - id (string)
  - query_id (trace_id)
  - part1_ancient (string, zh)
  - part2_modern (string, zh)
  - part3_closure (string, fixed: “——不如孔孟之道”)
  - safety_label (enum: pass/alter/reject)

- VoiceTiming
  - id (string)
  - satire_text_id (string)
  - audio_ref (uri)
  - timings: [{ start_ms, end_ms, phoneme|syllable }]

- RenderJob
  - id (string)
  - voice_timing_id (string)
  - status (enum: queued/running/succeeded/failed)
  - output_ref (uri)
  - created_at/updated_at (timestamp)

- Provenance
  - id (string)
  - query_id (trace_id)
  - model (string)
  - prompt_template_version (string)
  - sources: [{ passage_id, title, location }]
  - params (object)
  - latency_ms: { text, tts, render, end_to_end }

- SafetyReport
  - id (string)
  - query_id (trace_id)
  - risk (enum: low/medium/high)
  - action (enum: pass/alter/reject)
  - reason (string)

## Relationships

- Query 1‑to‑1 RetrievalSet
- Query 1‑to‑1 SatireText
- SatireText 1‑to‑1 VoiceTiming
- VoiceTiming 1‑to‑1 RenderJob
- Query 1‑to‑1 Provenance
- Query 1‑to‑1 SafetyReport

## Constraints & Validation

- Query.text: 中文输出要求；过长输入截断并提示重试。
- Passage.source/location: 必填；location 保持规范化（书/篇/章/行段）。
- RetrievalSet.items: 至少 1 条；Top‑3 命中率评测以 items[:3] 计算。
- SatireText: 必须包含三段，第三段固定文案；若无可靠出处，禁止伪造引用并明确标注。
- VoiceTiming.timings: 连续且不重叠，覆盖音频区间。
- RenderJob: 状态机如下。

## State Transitions (RenderJob)

- queued → running → succeeded | failed
- 失败允许一次重试；超过配额或速率限制应返回 429 而非进入排队。

