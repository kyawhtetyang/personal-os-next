"""Canonical execution result model for Personal OS Next."""
from __future__ import annotations


def success(capability, run_id=None, artifacts=None, data=None):
    return {
        "status": "success",
        "capability": capability,
        "run_id": run_id,
        "artifacts": artifacts or [],
        "data": data or {},
        "error": None,
    }


def failure(capability, error, run_id=None, artifacts=None, data=None):
    return {
        "status": "failed",
        "capability": capability,
        "run_id": run_id,
        "artifacts": artifacts or [],
        "data": data or {},
        "error": error,
    }


def validate_result(result):
    required = {"status", "capability", "run_id", "artifacts", "data", "error"}
    missing = required - set(result)
    if missing:
        raise ValueError(f"Result is missing required fields: {sorted(missing)}")
    if result["status"] not in {"success", "failed"}:
        raise ValueError("Result status must be success or failed.")
    if not isinstance(result["artifacts"], list):
        raise ValueError("Result artifacts must be a list.")
    if not isinstance(result["data"], dict):
        raise ValueError("Result data must be an object.")
    if result["status"] == "success" and result["error"] is not None:
        raise ValueError("Successful result must have error=None.")
    if result["status"] == "failed" and not isinstance(result["error"], dict):
        raise ValueError("Failed result must have an error object.")
    return result
