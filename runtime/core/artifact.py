"""Artifact registry support for Personal OS Next."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REGISTRY = Path("data/artifacts/registry/artifacts.json")


def _load(path):
    if not path.exists():
        return {"schema_version": "0.1", "artifacts": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _save(registry, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def register_artifact(path, artifact_type, run_id=None, source=None, registry_path=DEFAULT_REGISTRY):
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Artifact not found: {path}")

    registry_path = Path(registry_path)
    registry = _load(registry_path)
    record = {
        "artifact_id": str(uuid.uuid4()),
        "type": artifact_type,
        "path": str(path),
        "run_id": run_id,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    registry["artifacts"].append(record)
    _save(registry, registry_path)
    return record


def list_artifacts(registry_path=DEFAULT_REGISTRY):
    return _load(Path(registry_path))["artifacts"]


def get_artifact(artifact_id, registry_path=DEFAULT_REGISTRY):
    for artifact in list_artifacts(registry_path):
        if artifact["artifact_id"] == artifact_id:
            return artifact
    return None


def find_by_run(run_id, registry_path=DEFAULT_REGISTRY):
    return [
        artifact
        for artifact in list_artifacts(registry_path)
        if artifact["run_id"] == run_id
    ]
