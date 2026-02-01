# Personal AI Memory & Knowledge Store (v1)

## Overview

This module provides a deterministic, local memory store for persisting and retrieving explicitly written factual records across sessions.

It is an infrastructure component with no intelligence or autonomy.

## Core Responsibility

Persist structured records and return them only through explicit, exact-match queries.

## What This Module Does NOT Do

- Does not infer meaning
- Does not summarize or interpret data
- Does not learn or adapt behavior
- Does not decide relevance
- Does not execute actions
- Does not modify existing records automatically
- Does not observe the system autonomously

## Storage Model

- Local JSON file storage
- Human-readable format
- Append-only by default
- No automatic deletion or cleanup

## Folder Structure

```
MEMORY_STORE/
├── data/
│   └── memory.json
├── memory_store/
│   ├── __init__.py
│   ├── schemas.py
│   ├── storage.py
│   └── store.py
├── tests/
│   └── test_determinism.py
└── README.md
```

## Determinism Guarantees

- Same inputs produce the same outputs
- Records are returned in append order
- No randomness
- No internal clocks
- No environment-dependent behavior

## Limitations

- No semantic search
- No vector storage
- No relevance ranking
- No background processes
- No schema enforcement

## Usage

This module is intended to be imported and used as a library by other system components.

## Status

Implemented, tested, and locked (v1)
