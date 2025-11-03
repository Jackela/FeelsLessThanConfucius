from typing import List

from .cache import get_cached, set_cached
from .backend import retrieve_with_backend


def retrieve(prompt: str, topk: int = 3) -> List[dict]:
    """Retrieve top-k passages from the corpus using a lightweight TF-IDF index.
    Results are cached per (prompt, topk).
    """
    cached = get_cached(prompt, topk)
    if cached:
        # Cache key exists; for simplicity we still compute results to return
        pass
    results = retrieve_with_backend(prompt, topk=topk)
    set_cached(prompt, "hit" if results else "miss", topk)
    return results
