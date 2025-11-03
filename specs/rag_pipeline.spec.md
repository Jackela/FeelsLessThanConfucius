# rag_pipeline.spec.md

## Scope

Define retrieval pipeline for Four Books corpus with RAG contracts.

## Corpus & Chunking

- Sources: 论语、孟子、大学、中庸
- Chunk size: TBD (research-driven); overlap TBD
- Metadata: 书名、篇章、行/段、片段ID

## Retrieval Contract

- Input: `text` topic, `topk` (default 3)
- Output: list of passages: `{ passage_id, title, location, confidence }`

## Evaluation

- Offline eval set maintained under `specs/1-confucian-rag-agent/eval/`
- Weekly sampling of production prompts for replay
- Metric: Top-3 命中率 ≥ 85%

## Backend Selection

- Env: `RAG_BACKEND` (default `tfidf`, optional `faiss` if available)
- TF‑IDF: lightweight in‑process index (default)
- FAISS: planned integration; when enabled but unavailable, system gracefully falls back to TF‑IDF
