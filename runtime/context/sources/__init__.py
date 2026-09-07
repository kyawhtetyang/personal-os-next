"""Built-in deterministic context sources."""
from runtime.context.sources.artifacts import collect_artifacts
from runtime.context.sources.discovery import collect_discovery
from runtime.context.sources.state import collect_state
DEFAULT_SOURCES = {"state": collect_state, "discovery": collect_discovery, "artifacts": collect_artifacts}
