"""Execution record support for Personal OS runtime."""
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

def write_run(capability, status, source_url=None, artifact_path=None, error=None, runs_dir="data/runs"):
    run_id = str(uuid.uuid4())
    record = {
        "run_id": run_id,
        "capability": capability,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_url": source_url,
        "artifact_path": artifact_path,
        "error": error,
    }
    directory = Path(runs_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{run_id}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record
