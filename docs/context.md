# Context Layer

Personal OS Next v0.3.0 introduces a provider-independent Context Layer.

Context selects and assembles information relevant to a request. It is not a prompt, model integration, or knowledge store.

Lifecycle:
Consumer -> ContextRequest -> ContextAssembler -> state/discovery/artifacts -> Canonical Context -> JSON or Markdown projection

Assembly is deterministic and the core does not depend on an AI provider.

CLI:
python -m runtime context show --purpose development
python -m runtime context show --purpose development --format json
