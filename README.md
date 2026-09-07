# Personal OS Next

Personal OS Next is a capability-first, headless Personal Operating System.

## Core flow

Human / AI / CLI
→ Context
→ Capability
→ Runtime
→ Verification
→ Data

## Architecture

- vault/ — Human workspace, primarily Obsidian
- system/ — Rules, contracts, policies and capability definitions
- runtime/ — Execution implementations and canonical runtime behavior
- data/ — State, artifacts and run records
- ops/ — Maintenance
- tests/ — Quality
- docs/ — Architecture and documentation
- archive/ — Historical material

## Principle

Start deterministic and simple. Add workflows when repeated. Add dedicated orchestration only when real coordination problems justify it.

## Canonical execution

```bash
python -m runtime execute media.save \
  --input '{"url":"https://example.com/video"}' \
  --options '{"mode":"audio"}'
```

Vault access is Markdown-first through canonical vault.read and vault.write capabilities.\n\nHuman-friendly capability commands remain available as convenience adapters.

Status: v0.6.0 Vault Access Foundation.
