"""Central execution lifecycle."""
from __future__ import annotations

from pathlib import Path

from runtime.capabilities.media_save import save_media
from runtime.capabilities.vault_access import read_vault, write_vault
from runtime.core.artifact import register_artifact
from runtime.core.registry import get_capability
from runtime.core.result import failure, success, validate_result
from runtime.core.run_record import write_run
from runtime.core.state import update_state
from runtime.execution.errors import error
from runtime.execution.models import ExecutionContext, ExecutionRequest


class ExecutionEngine:
    """Execute registered capabilities through one canonical lifecycle."""

    def _resolve(self, capability):
        if get_capability(capability) is None:
            raise LookupError(f"Unknown capability: {capability}")
        handlers = {
            "media.save": save_media,
            "vault.read": read_vault,
            "vault.write": write_vault,
        }
        try:
            return handlers[capability]
        except KeyError as exc:
            raise LookupError(f"No runtime implementation for capability: {capability}") from exc

    def execute(self, request):
        try:
            if not isinstance(request, ExecutionRequest):
                request = ExecutionRequest.from_dict(request)
        except (TypeError, ValueError) as exc:
            return failure("unknown", error("ValidationError", str(exc)))

        context = ExecutionContext.create(request)

        try:
            handler = self._resolve(request.capability)
        except (LookupError, FileNotFoundError, ValueError) as exc:
            run = write_run(request.capability, "failed", error=error("ResolutionError", str(exc)))
            return failure(request.capability, error("ResolutionError", str(exc)), run_id=run["run_id"], data={"run": run})

        try:
            raw = handler(**request.input, **request.options)
            validate_result(raw)
        except Exception as exc:
            run = write_run(request.capability, "failed", error=error("ExecutionError", str(exc)))
            return failure(request.capability, error("ExecutionError", str(exc)), run_id=run["run_id"], data={"run": run})

        if raw["status"] == "failed":
            run = write_run(request.capability, "failed", error=raw["error"])
            raw["run_id"] = run["run_id"]
            raw["data"]["run"] = run
            return raw

        artifact = None
        artifact_path = raw["data"].get("artifact_path")
        if artifact_path:
            if not Path(artifact_path).is_file():
                err = error("VerificationError", "Capability reported an artifact path that was not found.")
                run = write_run(request.capability, "failed", error=err)
                return failure(request.capability, err, run_id=run["run_id"], data={"run": run})

        try:
            run = write_run(request.capability, "success", artifact_path=str(artifact_path) if artifact_path else None)
            if artifact_path:
                artifact = register_artifact(
                    artifact_path,
                    raw["data"].get("artifact_type", "artifact"),
                    run_id=run["run_id"],
                    source=raw["data"].get("source_url"),
                )
            state_updates = {
                "status": "success",
                "last_run_id": run["run_id"],
            }
            if artifact:
                state_updates.update({
                    "last_artifact_id": artifact["artifact_id"],
                    "last_artifact_path": str(artifact_path),
                })
            state = update_state(request.capability, state_updates)
        except Exception as exc:
            err = error("VerificationError", str(exc))
            return failure(request.capability, err, run_id=context.run_id)

        result = success(
            request.capability,
            run_id=run["run_id"],
            artifacts=[artifact] if artifact else [],
            data={**raw["data"], "run": run, "state": state, "context": {"run_id": context.run_id, "timestamp": context.timestamp}},
        )
        return validate_result(result)
