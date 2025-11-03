from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import List, Dict, Tuple


_corpus: List[Tuple[str, str, str]] = []  # (passage_id, title, text_with_location)
_built = False
_token_docs: List[List[str]] = []
_df: Dict[str, int] = {}


@dataclass
class Passage:
  passage_id: str
  title: str
  location: str
  text: str


def _default_corpus() -> List[Passage]:
    return [
        Passage(
            passage_id="analects-1-1",
            title="论语",
            location="学而·第一·第一章",
            text="子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？",
        ),
        Passage(
            passage_id="mencius-1-1",
            title="孟子",
            location="梁惠王上·第一章",
            text="孟子见梁惠王。王曰：叟，不远千里而来，亦将有以利吾国乎？",
        ),
        Passage(
            passage_id="daxue-1-1",
            title="大学",
            location="开篇",
            text="大学之道，在明明德，在亲民，在止于至善。",
        ),
        Passage(
            passage_id="zhongyong-1-1",
            title="中庸",
            location="开篇",
            text="天命之谓性，率性之谓道，修道之谓教。",
        ),
    ]


def _tokenize(text: str) -> List[str]:
    # Simple character-level tokens for CJK, remove punctuation/spaces
    text = re.sub(r"[\s，。、“”‘’！；：？,.!?;:()（）\-]+", "", text)
    return list(text)


def load_corpus(passages: List[Passage] | None = None) -> None:
    global _corpus
    if passages is None:
        passages = _default_corpus()
    _corpus = [(p.passage_id, p.title, f"{p.location}\n{p.text}") for p in passages]


def build_index() -> None:
    global _built, _token_docs, _df
    if not _corpus:
        load_corpus()
    _token_docs = []
    _df = {}
    for _, _, text in _corpus:
        toks = _tokenize(text)
        _token_docs.append(toks)
        seen = set(toks)
        for t in seen:
            _df[t] = _df.get(t, 0) + 1
    _built = True


def query(text: str, topk: int = 3) -> List[Dict]:
    if not _built:
        build_index()
    q_toks = _tokenize(text)
    if not q_toks:
        return []
    scores: List[Tuple[int, float]] = []
    N = len(_token_docs)
    q_tf: Dict[str, int] = {}
    for t in q_toks:
        q_tf[t] = q_tf.get(t, 0) + 1
    # Compute simple TF-IDF cosine similarity
    def idf(t: str) -> float:
        df = _df.get(t, 0)
        return math.log((N + 1) / (df + 1)) + 1.0

    q_vec: Dict[str, float] = {t: (tf * idf(t)) for t, tf in q_tf.items()}
    q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0

    for idx, toks in enumerate(_token_docs):
        d_tf: Dict[str, int] = {}
        for t in toks:
            d_tf[t] = d_tf.get(t, 0) + 1
        d_vec: Dict[str, float] = {t: (tf * idf(t)) for t, tf in d_tf.items() if t in q_vec}
        if not d_vec:
            scores.append((idx, 0.0))
            continue
        dot = sum(q_vec[t] * d_vec.get(t, 0.0) for t in q_vec)
        d_norm = math.sqrt(sum(v * v for v in d_vec.values())) or 1.0
        sim = dot / (q_norm * d_norm)
        scores.append((idx, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    out: List[Dict] = []
    for idx, sc in scores[: max(1, topk)]:
        pid, title, text = _corpus[idx]
        # Split back to location + text
        parts = text.split("\n", 1)
        location = parts[0]
        out.append(
            {
                "passage_id": pid,
                "title": title,
                "location": location,
                "confidence": round(float(sc), 3),
            }
        )
    return out
