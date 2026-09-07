# v0.1.0 Quality Gate

Before release:

- Python package imports successfully
- Unit tests pass
- CLI help works
- health check works
- media.save validates prerequisites
- success creates an artifact
- success creates a run record
- failure creates a run record
- documentation matches commands

Run:

```bash
python -m unittest discover -s tests -v
python -m runtime --help
python -m runtime health check
```
