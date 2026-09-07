# Data Layer

## Purpose

The data layer preserves machine-facing operational truth.

## Structure

- state/ — current machine-readable state
- artifacts/ — generated outputs
- runs/ — execution records

Flow:

REQUEST
→ EXECUTE
→ VERIFY
→ ARTIFACT
→ RUN RECORD

Run records allow humans and AI models to inspect execution history without depending on chat history.
