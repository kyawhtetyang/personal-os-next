"""Canonical context models for Personal OS Next."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class ContextRequest:
    purpose: str
    query: str | None = None
    sources: list[str] | None = None
    options: dict = field(default_factory=dict)
    def __post_init__(self):
        if not isinstance(self.purpose, str) or not self.purpose.strip(): raise ValueError("Context purpose must be a non-empty string.")
        if self.query is not None and not isinstance(self.query, str): raise ValueError("Context query must be a string or None.")
        if self.sources is not None and (not isinstance(self.sources, list) or not all(isinstance(source, str) and source for source in self.sources)): raise ValueError("Context sources must be a list of non-empty strings.")
        if not isinstance(self.options, dict): raise ValueError("Context options must be an object.")
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, payload):
        if not isinstance(payload, dict): raise ValueError("Context request must be an object.")
        return cls(**payload)

@dataclass
class Context:
    id: str
    created_at: str
    purpose: str
    sources: list[str]
    data: dict
    metadata: dict = field(default_factory=dict)
    @classmethod
    def create(cls, request, data, sources):
        return cls(f"ctx_{uuid.uuid4().hex}", datetime.now(timezone.utc).isoformat(), request.purpose, list(sources), data, {"query": request.query} if request.query else {})
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, payload):
        if not isinstance(payload, dict): raise ValueError("Context must be an object.")
        return cls(**payload)
