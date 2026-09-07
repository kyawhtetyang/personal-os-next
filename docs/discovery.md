# Discovery Protocol

## Purpose

Discovery provides one canonical entry point for an interface, AI model, or runtime client to understand Personal OS Next.

## Entry points

Machine-readable manifest:

```text
system/discovery/manifest.json
```

Runtime command:

```bash
python -m runtime discover
```

## Discovery flow

```text
Client
  ↓
Discovery Manifest
  ↓
Version
Architecture
Capabilities
Contracts
Entrypoints
  ↓
Capability Registry
  ↓
Definition + Contract
  ↓
Runtime Execution
```

## Design principle

Discovery describes the OS. It does not execute capabilities.

Execution remains inside the runtime boundary.
