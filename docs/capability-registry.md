# Capability Registry

## Purpose

The Capability Registry is the canonical machine-readable answer to:

> What can Personal OS Next do?

## Canonical source

```text
system/capabilities/registry.json
```

## Registry entry

Each capability entry contains:

- `id` — stable canonical identifier
- `status` — lifecycle status
- `version` — capability contract version
- `definition` — human-readable capability definition
- `contract` — machine-readable contract
- `runtime` — implementation module
- `cli` — canonical command entrypoint
- `description` — short discovery description

## Design rule

```text
JSON
  = canonical discovery data

Markdown
  = human explanation

Contract JSON
  = machine interface definition

Runtime
  = executable implementation
```

Do not duplicate full capability specifications in the registry. The registry points to the canonical definition and contract.

## Lookup flow

```text
Request
  ↓
Capability Registry
  ↓
Capability ID
  ↓
Definition + Contract
  ↓
Runtime / CLI
  ↓
Execution
```
