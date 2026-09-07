# Changelog

All notable changes to Personal OS Next are documented here.

## [0.3.0] - 2026-09-07

### Added
- Provider-independent canonical Context model.
- ContextRequest with serialization support.
- Deterministic ContextAssembler.
- Built-in state, discovery, and artifact context sources.
- JSON and Markdown context projections.
- CLI context access through python -m runtime context show.
- Focused Context Layer tests and documentation.

### Boundaries
- No AI provider integration.
- No semantic retrieval, vector database, RAG, agents, or workflow engine.
- Context remains a selection and representation layer over existing OS data.

## [0.1.0] - 2026-09-07

### Added
- Canonical Personal OS Next architecture
- Governance principles and system boundaries
- AI handoff guidance through AGENTS.md
- Python runtime package and canonical CLI
- Runtime health checks
- Capability definitions and contracts
- media.save capability for media download and conversion
- Persistent run records
- Data layer documentation
- Quality gate
- Unit tests

## [0.2.0] - 2026-09-07

### Added
- Persistent runtime state model.
- Artifact registry for generated artifacts.
- Canonical execution result model.
- Capability registry and runtime capability discovery.
- System discovery manifest and runtime discovery command.
- Execution lifecycle integration between runs, artifacts, and state.
- Integration and end-to-end validation coverage.

### Validation
- 29 automated tests passing.
- Quality checks passing.
- Health checks passing.
- Real end-to-end media.save execution validated.
