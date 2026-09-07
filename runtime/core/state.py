"""Small persistent state primitive for Personal OS Next."""
from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STATE = Path("data/state/runtime.json")


def _load(path):
    if not path.exists():
        return {"schema_version": "0.1", "updated_at": None, "state": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def _save(payload, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def get_state(key, state_path=DEFAULT_STATE):
    payload = _load(Path(state_path))
    value = payload["state"].get(key)
    return deepcopy(value)


def set_state(key, value, state_path=DEFAULT_STATE):
    if not isinstance(value, dict):
        raise ValueError("State value must be an object.")

    path = Path(state_path)
    payload = _load(path)
    payload["state"][key] = deepcopy(value)
    _save(payload, path)
    return get_state(key, path)


def update_state(key, updates, state_path=DEFAULT_STATE):
    if not isinstance(updates, dict):
        raise ValueError("State updates must be an object.")

    current = get_state(key, state_path) or {}
    current.update(deepcopy(updates))
    return set_state(key, current, state_path)


def delete_state(key, state_path=DEFAULT_STATE):
    path = Path(state_path)
    payload = _load(path)
    existed = key in payload["state"]
    payload["state"].pop(key, None)
    _save(payload, path)
    return existed


def list_state(state_path=DEFAULT_STATE):
    payload = _load(Path(state_path))
    return deepcopy(payload["state"])
