# Execution Architecture

The Execution Layer is the canonical runtime orchestration boundary.

## Lifecycle

```text
ExecutionRequest
  -> validate
  -> resolve capability
  -> create context
  -> execute capability-specific work
  -> verify artifact
  -> record run
  -> register artifact
  -> update state
  -> Canonical Result
```

Capabilities perform capability-specific work. The ExecutionEngine owns shared runtime orchestration.

## Models

ExecutionRequest contains capability, input, and optional options.

ExecutionContext contains run_id, capability, timestamp, and request.

## Boundaries

No workflow engine, scheduler, automation, AI routing, parallel execution, distributed workers, or database migration is included.
