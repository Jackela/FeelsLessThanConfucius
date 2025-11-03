from .provenance_service import cleanup_retention


def run_cleanup() -> int:
    """Remove expired provenance records (>=30 days). Returns deleted count."""
    return cleanup_retention(30)

