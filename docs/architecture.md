# Personal OS Next Architecture

Personal OS Next is a headless system with clear boundaries.

HUMAN / CLI / API / AI
        |
        v
     Context Layer
        |
        v
System Discovery / State / Artifacts / Capabilities
        |
        v
     Runtime
        |
        v
      Data

## Layers

- vault/ is the human workspace.
- system/ contains rules, contracts, capabilities, and discovery metadata.
- runtime/ contains executable system behavior.
- data/ contains persistent state, artifacts, and run records.
- context/ selects and projects relevant information for consumers without depending on an AI provider.

## v0.3 Context Flow

Consumer -> ContextRequest -> ContextAssembler -> Sources -> Canonical Context -> Projection

Context is not a knowledge store, prompt, or model adapter.
