# Agent Task Decomposer (v1)

## Overview

**Agent Task Decomposer (v1)** is a **planning-only** system that converts a high-level user goal into a **deterministic, ordered list of atomic tasks**.

The module **does not execute anything**. It produces **planning data only**, designed to be consumed by downstream systems such as executors, validators, or permission gates.

This project is intentionally strict, minimal, and auditable.

---

## What This Project Does

* Accepts a structured user goal
* Decomposes it into **atomic tasks**
* Guarantees **deterministic output**
* Returns a **machine-readable plan** or a **silent failure**

---

## What This Project Explicitly Does NOT Do

* Execute tasks
* Access filesystem, OS, or network
* Infer user intent or permissions
* Perform safety, risk, or feasibility checks
* Retry, optimize, or revise plans
* Learn or adapt over time

This is a **pure planner**, not an agent executor.

---

## Core Design Principles

### 1. Planning Only

The system produces **descriptions of actions**, not actions themselves.

### 2. Atomicity

Each task represents **exactly one real-world action** with:

* No internal sequencing
* No branching or conditions
* No retries
* No hidden logic

### 3. Determinism

Identical input **always** produces **byte-identical output**.

### 4. Silent Failure

If a goal cannot be decomposed under the rules:

* No errors are thrown
* No partial plans are returned
* Output contains an empty task list

---

## Input Schema

```json
{
  "goal_id": "string",
  "user_goal": "string",
  "context": {
    "available_tools": [],
    "workspace_paths": [],
    "constraints": []
  }
}
```

Notes:

* `context` is **read-only** in v1
* No field implies permission or executability

---

## Output Schema

```json
{
  "plan_id": "string",
  "tasks": []
}
```

* `plan_id` is always present
* `tasks` may be empty (silent failure)

---

## Atomic Task Schema

```json
{
  "task_id": "string",
  "task_type": "ENUM",
  "task_parameters": {},
  "depends_on": []
}
```

Rules:

* All fields are mandatory
* `depends_on` must exist even if empty
* No free-text descriptions allowed

---

## Supported Task Types (v1)

The system supports a **closed set** of atomic actions:

* CREATE_FILE
* WRITE_FILE
* DELETE_FILE
* CREATE_DIRECTORY
* DELETE_DIRECTORY
* OPEN_APPLICATION
* CLOSE_APPLICATION
* SEND_NETWORK_REQUEST
* RECEIVE_NETWORK_RESOURCE

If an action does not fit **exactly one** of these types, it is **not representable in v1**.

---

## Failure Semantics

If decomposition is not possible:

```json
{
  "plan_id": "string",
  "tasks": []
}
```

No error messages. No partial plans.

---

## Example (Successful Decomposition)

```json
{
  "plan_id": "plan::ex1::create file /tmp/a.txt",
  "tasks": [
    {
      "task_id": "plan::ex1::create file /tmp/a.txt::task::0",
      "task_type": "CREATE_FILE",
      "task_parameters": {
        "path": "/tmp/a.txt"
      },
      "depends_on": []
    }
  ]
}
```

---

## Example (Silent Failure)

```json
{
  "plan_id": "plan::ex3::delete all files in tmp",
  "tasks": []
}
```

---

## Project Structure

```
agent_task_decomposer/
│
├── decomposer/
│   ├── models.py
│   ├── task_types.py
│   ├── id_strategy.py
│   ├── atomicity_rules.py
│   ├── validator.py
│   └── decomposer.py
│
├── tests/
│   ├── test_decomposition.py
│   ├── test_determinism.py
│   └── test_atomicity.py
│
└── examples/
```

Each file maps to **exactly one architectural responsibility**.

---

## Why This Design Matters

Most agent systems fail due to:

* Hidden execution
* Non-determinism
* Overloaded task abstractions
* Implicit reasoning

This project avoids those failures by enforcing:

* Constraint-first design
* Atomic task laws
* Deterministic identity
* Silent, explicit failure

---

## Versioning

* **v1**: Strict, minimal, single-task decomposition
* Any expansion (multi-task plans, new task types) requires **v2**

---

## One-Line Summary

> A deterministic planning module that converts high-level goals into strictly atomic, machine-readable task plans without executing or inferring intent.
