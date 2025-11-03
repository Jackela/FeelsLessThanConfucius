import os
from typing import List, Dict

from .index import query as tfidf_query


def get_backend_name() -> str:
    return os.getenv("RAG_BACKEND", "tfidf").lower()


def retrieve_with_backend(prompt: str, topk: int = 3) -> List[Dict]:
    backend = get_backend_name()
    if backend == "tfidf":
        return tfidf_query(prompt, topk=topk)
    elif backend == "faiss":
        # Optional FAISS backend hook. Fallback to TF-IDF if FAISS not available.
        try:
            import faiss  # type: ignore
            # NOTE: Real FAISS integration not implemented in this scaffold.
            # Use TF-IDF temporarily.
            return tfidf_query(prompt, topk=topk)
        except Exception:
            return tfidf_query(prompt, topk=topk)
    else:
        # Unknown backend — use TF-IDF
        return tfidf_query(prompt, topk=topk)

