# Access Layer

Personal OS Next exposes stable system behavior through simple access patterns.

## Canonical execution

All capability execution uses the same request shape:

```text
ExecutionRequest
  capability
  input
  options
      ↓
ExecutionEngine
```

CLI:

```bash
python -m runtime execute media.save \
  --input '{"url":"https://example.com/video"}' \
  --options '{"mode":"audio","audio_format":"mp3"}'
```

The generic command is the canonical access path for AI clients and future interfaces.

## Convenience commands

Human-friendly commands remain available:

```bash
python -m runtime media save URL
python -m runtime discover
python -m runtime capabilities list
python -m runtime capabilities show media.save
python -m runtime context show --purpose "..."
python -m runtime health check
```

Convenience commands adapt user input to existing canonical models. They do not create separate execution lifecycles.

## Access principle

```text
Human / AI / CLI / Future API
           ↓
    Canonical models
           ↓
     Runtime core
```

The Access Layer does not own capability routing, execution orchestration, or business logic. Those remain in existing runtime components.
