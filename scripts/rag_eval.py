"""
Weekly RAG evaluation script (stub).
Reads eval prompts from specs/1-confucian-rag-agent/eval/README.md if present.
Computes a placeholder Top-3 hit rate using the current retrieve() stub.
"""
from pathlib import Path
from typing import List

from src.rag.query import retrieve


def load_eval_prompts() -> List[str]:
    eval_file = Path("specs/1-confucian-rag-agent/eval/README.md")
    if not eval_file.exists():
        return ["仁义礼智信", "修身齐家治国平天下"]
    prompts: List[str] = []
    for line in eval_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            prompts.append(line)
    return prompts


def compute_top3_hit_rate(prompts: List[str]) -> float:
    # With current stub retrieve() returning at least one result, this is 1.0
    # Replace with real metric once FAISS is wired.
    hits = 0
    for p in prompts:
        results = retrieve(p, topk=3)
        hits += 1 if results else 0
    return hits / max(1, len(prompts))


def main() -> None:
    prompts = load_eval_prompts()
    rate = compute_top3_hit_rate(prompts)
    print({"prompts": len(prompts), "top3_hit_rate": rate})
    if rate < 0.85:
        raise SystemExit("Top-3 hit rate below 0.85 threshold")


if __name__ == "__main__":
    main()

