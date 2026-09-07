# Personal OS Next Architecture

Personal OS Next is a headless, capability-first system with clear boundaries.

```text
HUMAN / AI / CLI / FUTURE API
             |
             v
        Access Layer
             |
             v
       Context Layer
             |
             v
Capabilities / Discovery / State / Artifacts
             |
             v
      Execution Engine
             |
             v
          Runtime
             |
             v
           Data
```

## Layers

- vault/ is the human workspace.
- system/ contains rules, contracts, capabilities, and discovery metadata.
- runtime/ contains executable system behavior.
- data/ contains persistent state, artifacts, and run records.
- context/ selects and projects relevant information without depending on an AI provider.

## Canonical execution

```text
Client
  ↓
ExecutionRequest
  ↓
ExecutionEngine
  ↓
Capability
  ↓
Verification
  ↓
Run + Artifact + State
  ↓
Canonical Result
```

## Access Layer

The generic CLI command is the canonical execution access path:

```bash
python -m runtime execute <capability> --input '<json>' --options '<json>'
```

Specialized commands such as `media save` remain convenience adapters. They translate user-friendly arguments into canonical request models and use the same ExecutionEngine lifecycle.

The Access Layer does not introduce a new router, planner, orchestrator, or execution model.

## Context

```text
Consumer
  ↓
ContextRequest
  ↓
ContextAssembler
  ↓
Sources
  ↓
Canonical Context
  ↓
Projection
```

Context is not a knowledge store, prompt, or model adapter.
