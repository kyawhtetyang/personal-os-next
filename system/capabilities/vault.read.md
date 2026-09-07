# vault.read

Read one Markdown file from the canonical vault.

## Input
- path: relative Markdown path inside vault/

## Output
- path
- content
- format

## Rules
- Paths must remain inside vault/.
- Absolute paths and traversal outside vault/ are rejected.
- Only Markdown files are supported in this version.