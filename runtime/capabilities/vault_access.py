"""Capability-specific work for canonical vault access."""
from __future__ import annotations

from pathlib import Path

from runtime.core.result import failure, success

VAULT_ROOT = Path("vault")


def _fail(kind, message, hint=None):
    return failure("vault.access", {"kind": kind, "message": message, "hint": hint}, data={})


def resolve_vault_path(path, vault_root=VAULT_ROOT):
    root = Path(vault_root).resolve()
    candidate = Path(path)
    if candidate.is_absolute():
        raise ValueError("Vault path must be relative to the vault root.")
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Vault path escapes the vault root.") from exc
    return resolved


def read_vault(path, vault_root=VAULT_ROOT):
    try:
        target = resolve_vault_path(path, vault_root)
    except ValueError as exc:
        return failure("vault.read", {"kind": "ValidationError", "message": str(exc)}, data={})
    if target.suffix.lower() != ".md":
        return failure("vault.read", {"kind": "ValidationError", "message": "Vault access is Markdown-first; path must end in .md."}, data={})
    if not target.is_file():
        return failure("vault.read", {"kind": "NotFoundError", "message": f"Vault file not found: {path}"}, data={})
    content = target.read_text(encoding="utf-8")
    return success("vault.read", data={"path": str(target.relative_to(Path(vault_root).resolve())), "content": content, "format": "markdown"})


def write_vault(path, content, overwrite=False, vault_root=VAULT_ROOT):
    try:
        target = resolve_vault_path(path, vault_root)
    except ValueError as exc:
        return failure("vault.write", {"kind": "ValidationError", "message": str(exc)}, data={})
    if target.suffix.lower() != ".md":
        return failure("vault.write", {"kind": "ValidationError", "message": "Vault access is Markdown-first; path must end in .md."}, data={})
    if not isinstance(content, str):
        return failure("vault.write", {"kind": "ValidationError", "message": "content must be a string."}, data={})
    if target.exists() and not overwrite:
        return failure("vault.write", {"kind": "ConflictError", "message": f"Vault file already exists: {path}"}, data={})
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    if target.read_text(encoding="utf-8") != content:
        return failure("vault.write", {"kind": "VerificationError", "message": "Vault content verification failed."}, data={})
    return success("vault.write", data={"path": str(target.relative_to(Path(vault_root).resolve())), "bytes_written": len(content.encode("utf-8")), "format": "markdown"})