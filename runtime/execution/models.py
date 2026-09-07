"""Execution request and context models."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class ExecutionRequest:
    capability: str
    input: dict
    options: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.capability, str) or not self.capability.strip():
            raise ValueError("capability must be a non-empty string.")
        if not isinstance(self.input, dict):
            raise ValueError("input must be an object.")
        if not isinstance(self.options, dict):
            raise ValueError("options must be an object.")

    def to_dict(self):
        return {"capability": self.capability, "input": dict(self.input), "options": dict(self.options)}

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict):
            raise ValueError("ExecutionRequest must be an object.")
        return cls(value.get("capability"), value.get("input"), value.get("options") or {})


@dataclass
class ExecutionContext:
    run_id: str
    capability: str
    timestamp: str
    request: ExecutionRequest

    @classmethod
    def create(cls, request):
        return cls(
            run_id=str(uuid.uuid4()),
            capability=request.capability,
            timestamp=datetime.now(timezone.utc).isoformat(),
            request=request,
        )
