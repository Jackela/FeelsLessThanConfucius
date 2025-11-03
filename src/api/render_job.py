from dataclasses import dataclass
from typing import Dict


@dataclass
class RenderJob:
    id: str
    status: str  # queued/running/succeeded/failed
    output_ref: str | None = None


_jobs: Dict[str, RenderJob] = {}


def save_job(job: RenderJob) -> None:
    _jobs[job.id] = job


def get_job(job_id: str) -> RenderJob | None:
    return _jobs.get(job_id)

