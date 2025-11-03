from typing import Dict, Tuple


_cache: Dict[Tuple[str, int], str] = {}


def get_cached(prompt: str, topk: int = 3) -> str | None:
    return _cache.get((prompt, topk))


def set_cached(prompt: str, value: str, topk: int = 3) -> None:
    _cache[(prompt, topk)] = value

