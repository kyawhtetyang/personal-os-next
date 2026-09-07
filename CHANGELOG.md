# Changelog

All notable changes to Personal OS Next are documented here.

## [0.4.0] - 2026-09-08

### Added
- Central ExecutionEngine with one canonical execute() lifecycle.
- ExecutionRequest and ExecutionContext models with request serialization.
- Canonical validation, resolution, execution, and verification error handling.
- Focused execution model and lifecycle tests.
- Execution architecture documentation.

### Changed
- media.save now performs capability-specific work while ExecutionEngine owns run records, artifact registration, state updates, and canonical result orchestration.
- CLI media execution routes through the ExecutionEngine.

## [0.3.0] - 2026-09-07

### Added
- Provider-independent canonical Context model.
- ContextRequest with serialization support.
- Deterministic ContextAssembler.
- Built-in state, discovery, and artifact context sources.
- JSON and Markdown context projections.
- CLI context access through python -m runtime context show.
- Focused Context Layer tests and documentation.

## [0.2.0] - 2026-09-07

### Added
- Persistent runtime state model.
- Artifact registry for generated artifacts.
- Canonical execution result model.
- Capability registry and runtime capability discovery.
- System discovery manifest and runtime discovery command.
- Execution lifecycle integration between runs, artifacts, and state.

## [0.1.0] - 2026-09-07

### Added
- Canonical Personal OS Next architecture.
- Governance principles and system boundaries.
- Python runtime package and canonical CLI.
- Runtime health checks.
- media.save capability and persistent run records.
