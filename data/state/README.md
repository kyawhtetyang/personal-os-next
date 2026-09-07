# Runtime State

Runtime state stores current system truth.

Examples:

- last successful execution
- current status
- latest artifact reference

Canonical generated file:

```text
data/state/runtime.json
```

Do not treat state as history. Historical execution belongs in `data/runs/`.
