"""Deterministic context assembly for Personal OS Next."""
from runtime.context.models import Context, ContextRequest
from runtime.context.sources import DEFAULT_SOURCES

class ContextAssembler:
    def __init__(self, sources=None):
        self.sources = dict(DEFAULT_SOURCES)
        if sources: self.sources.update(sources)
    def assemble(self, request):
        if isinstance(request, dict): request = ContextRequest.from_dict(request)
        if not isinstance(request, ContextRequest): raise ValueError("Context request must be a ContextRequest or object.")
        requested = request.sources or list(self.sources)
        data, used = {}, []
        for name in requested:
            collector = self.sources.get(name)
            if collector is None: raise ValueError(f"Unknown context source: {name}")
            data[name] = collector(request)
            used.append(name)
        return Context.create(request, data, used)
