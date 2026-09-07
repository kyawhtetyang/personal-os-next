"""Self-discovery support for Personal OS Next."""
from __future__ import annotations

import json
from pathlib import Path

from runtime.core.registry import list_capabilities


DEFAULT_MANIFEST = Path("system/discovery/manifest.json")


def load_manifest(manifest_path=DEFAULT_MANIFEST):
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Discovery manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def discover(manifest_path=DEFAULT_MANIFEST, version_path=Path("VERSION")):
    manifest = load_manifest(manifest_path)
    version_file = Path(version_path)
    version = version_file.read_text(encoding="utf-8").strip()

    return {
        "status": "success",
        "os": manifest["os"],
        "version": version,
        "architecture": manifest["architecture"],
        "capabilities": [
            {
                "id": capability["id"],
                "status": capability["status"],
                "version": capability["version"],
                "description": capability["description"],
            }
            for capability in list_capabilities(
                manifest["capability_registry"]
            )
        ],
        "contracts": {
            "result": manifest["result_contract"]
        },
        "entrypoints": manifest["entrypoints"],
    }
