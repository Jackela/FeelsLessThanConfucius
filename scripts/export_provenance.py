"""
Export provenance records to JSONL (stdout or file).
Usage:
  python scripts/export_provenance.py > exports/provenance.jsonl
"""
import json
from typing import Iterable

from src.api.provenance_service import _store


def iter_records() -> Iterable[dict]:
    for item in _store.values():
        yield {**item.data, "created_at": item.created_at.isoformat()}


def main() -> None:
    for rec in iter_records():
        print(json.dumps(rec, ensure_ascii=False))


if __name__ == "__main__":
    main()

