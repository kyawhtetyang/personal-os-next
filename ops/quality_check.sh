#!/usr/bin/env bash
set -e
python -m unittest discover -s tests -v
python -m runtime --help
python -m runtime health check
