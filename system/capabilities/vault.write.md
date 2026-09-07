# vault.write

Write one Markdown file to the canonical vault.

## Input
- path: relative Markdown path inside vault/
- content: UTF-8 text
- overwrite: optional boolean, default false

## Output
- path
- bytes_written
- format

## Rules
- Paths must remain inside vault/.
- Absolute paths and traversal outside vault/ are rejected.
- Only Markdown files are supported in this version.
- Existing files are not replaced unless overwrite is true.
- Written content is read back for deterministic verification.