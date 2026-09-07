# Artifact Registry

## Purpose

The Artifact Registry is the canonical index of files produced by Personal OS Next.

A filesystem path tells the OS where a file is.

An artifact record tells the OS:

- what the file is
- which run produced it
- where it is stored
- where it came from
- when it was registered

## Flow

```text
Capability
  ↓
Produced file
  ↓
Artifact registration
  ↓
artifact_id
  ↓
Artifact Registry
```

## Artifact record

```text
artifact_id
type
path
run_id
source
created_at
```

## Scope

v0.2.0 introduces registry primitives first.

Automatic registration by every capability will be completed as part of the execution integration work, rather than duplicating registration logic inside each capability now.
