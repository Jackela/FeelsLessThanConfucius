from typing import Dict, Any


def build_audit_summary(provenance: Dict[str, Any]) -> Dict[str, Any]:
    sources = provenance.get("sources", [])
    return {
        "trace_id": provenance.get("trace_id"),
        "source_count": len(sources),
        "model": provenance.get("model"),
        "template_version": provenance.get("prompt_template_version"),
        "latency_ms": provenance.get("latency_ms", {}),
        "confidence": provenance.get("confidence"),
    }

