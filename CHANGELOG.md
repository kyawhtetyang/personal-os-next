# Changelog

All notable changes to Personal OS Next are documented here.

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

### Verified

- 5/5 unit tests passing
- Python runtime available
- yt-dlp available
- ffmpeg available
- Real YouTube audio download
- Real MP3 conversion
- Artifact creation
- Run record creation

[0.1.0]: https://github.com/kyawhtetyang/personal-os-next/releases/tag/v0.1.0

## [0.2.0] - 2026-09-07

### Added
- Persistent runtime state model.
- Artifact registry for generated artifacts.
- Canonical execution result model.
- Capability registry and runtime capability discovery.
- System discovery manifest and `python -m runtime discover`.
- Execution lifecycle integration between runs, artifacts, and state.
- Integration and end-to-end validation coverage.

### Fixed
- Runtime-generated state files are ignored by Git.
- Media artifact verification accepts artifacts reported by successful execution.

### Validation
- 29 automated tests passing.
- Quality checks passing.
- Health checks passing.
- Real end-to-end `media.save` execution validated.
