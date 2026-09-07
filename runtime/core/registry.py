"""Capability registry access for Personal OS Next."""
from __future__ import annotations

import json
from pathlib import Path


DEFAULT_REGISTRY = Path("system/capabilities/registry.json")


def load_capabilities(registry_path=DEFAULT_REGISTRY):
    """Load and validate the canonical capability registry."""
    path = Path(registry_path)
    if not path.exists():
        raise FileNotFoundError(f"Capability registry not found: {path}")

    registry = json.loads(path.read_text(encoding="utf-8"))
    capabilities = registry.get("capabilities")

    if not isinstance(capabilities, list):
        raise ValueError("Capability registry must contain a capabilities list.")

    ids = []
    for capability in capabilities:
        if not isinstance(capability, dict) or not capability.get("id"):
            raise ValueError("Each capability must be an object with an id.")
        ids.append(capability["id"])

    if len(ids) != len(set(ids)):
        raise ValueError("Capability registry contains duplicate ids.")

    return registry


def list_capabilities(registry_path=DEFAULT_REGISTRY):
    """Return all registered capabilities."""
    return load_capabilities(registry_path)["capabilities"]


def get_capability(capability_id, registry_path=DEFAULT_REGISTRY):
    """Return one capability by canonical id."""
    for capability in list_capabilities(registry_path):
        if capability["id"] == capability_id:
            return capability
    return None
