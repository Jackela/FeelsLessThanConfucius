from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="", tags=["provenance"])


from ..schemas import Provenance as ProvModel
from ..provenance_service import get_provenance as _get_prov


@router.get("/provenance/{trace_id}", response_model=ProvModel)
def get_provenance(trace_id: str):
    data = _get_prov(trace_id, retention_days=30)
    if not data:
        raise HTTPException(status_code=404, detail="Record not found or expired")
    return data
