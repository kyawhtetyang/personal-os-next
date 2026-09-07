# State Model

## Purpose

State represents what is currently true about the system.

## Distinction

```text
Run
= historical execution event

Artifact
= produced output

State
= current truth
```

## Storage

```text
data/state/runtime.json
```

The file is generated runtime data and should not be committed.

## API

```text
get_state(key)
set_state(key, value)
update_state(key, updates)
delete_state(key)
list_state()
```

## Design rule

State is intentionally a small JSON primitive in v0.2.0.

Do not introduce a database, event store, or memory framework until real requirements require them.

## Example

```json
{
  "media.save": {
    "status": "success",
    "last_run_id": "run-123",
    "last_artifact_id": "artifact-456"
  }
}
```
