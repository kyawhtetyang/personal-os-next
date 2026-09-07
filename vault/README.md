# Vault

Human-facing workspace.

Primary interface: Obsidian.

Contains human-authored notes, journals, projects and knowledge.

## Canonical access

Vault access is Markdown-first and capability-based:

- `vault.read` — read one Markdown file using a path relative to `vault/`.
- `vault.write` — write one verified Markdown file using a path relative to `vault/`.

Paths cannot escape the vault boundary. Existing files are not overwritten unless explicitly requested.

Runtime code, machine state, and generated artifacts should not be mixed into the vault by default.
