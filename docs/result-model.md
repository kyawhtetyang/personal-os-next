# Standard Result Model

## Purpose

Every capability returns one canonical execution envelope.

## Shape

```json
{
  "status": "success|failed",
  "capability": "string",
  "run_id": "string|null",
  "artifacts": [],
  "data": {},
  "error": null
}
```

## Boundary rule

```text
Runtime implementation
        ↓
Canonical Result Model
        ↓
CLI / AI / API / future interface
```

Capability-specific values belong in `data`. Produced files belong in `artifacts`.

## Status rule

- `success` → `error` must be `null`
- `failed` → `error` must be an object

## Migration

v0.2.0 introduces the core model first. Existing capabilities are migrated incrementally to avoid rewriting working execution paths.
