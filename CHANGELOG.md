# Changelog

All notable changes to Personal OS Next are documented here.

## [0.6.0] - 2026-09-08

### Added
- Canonical Markdown-first vault.read and vault.write capabilities.
- Safe vault path resolution that rejects absolute paths and vault escape attempts.
- Deterministic write verification and overwrite protection.
- ExecutionEngine support for successful non-artifact capabilities.
- Focused vault access tests.

### Changed
- Successful capabilities may now return canonical results without requiring an artifact.

## [0.5.0] - 2026-09-08

### Added
- Canonical generic CLI execution through `python -m runtime execute <capability>`.
- JSON object parsing for canonical `input` and optional `options`.
- Access Layer documentation for human, AI, CLI, and future API clients.

### Changed
- Existing human-friendly commands remain convenience adapters over canonical runtime models.
- README status and execution examples now reflect the current architecture.

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
