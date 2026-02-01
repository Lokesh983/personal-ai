# Project 6 — Personal AI Brain (v1)

## Overview

The Personal AI Brain (v1) is a deterministic orchestration module that coordinates task decomposition, safety validation, and execution by invoking external modules in a fixed sequence. It acts strictly as a control layer and does not perform planning, safety decisions, or execution itself.

---

## Core Responsibility

### What this module does
- Accepts structured user input
- Performs mechanical input normalization
- Invokes a task decomposer to obtain tasks
- For each task, invokes a guardrail check and, if approved, an executor
- Halts immediately on failure or confirmation requirement
- Produces a single, schema-defined final output

### What this module explicitly does NOT do
- Perform task planning or decomposition logic
- Make safety or approval decisions
- Execute real-world actions
- Retry failed steps
- Modify or infer task content
- Maintain state, memory, or learning
- Explain or justify decisions

---

## High-Level Execution Flow

1. Receive input containing a `user_input` string
2. Normalize input mechanically (whitespace trimming only)
3. Call the task decomposer with wrapped input
4. If no tasks are returned, stop and return failure
5. For each task:
   - Call the guardrail engine
   - If rejected, stop and return failure
   - If confirmation is required, stop and return confirmation status
   - If approved, call the action executor
   - If execution fails, stop and return failure
   - Record successful execution outcome
6. If all tasks succeed, return completed status with executed actions

---

## Module Interactions

The module invokes the following externally defined functions, which are expected to be provided at runtime:

- `task_decomposer(input_data)`
- `guardrail_engine(task)`
- `action_executor(task)`

These functions are declared in the code as external contracts and are not implemented within this repository.

---

## Folder Structure

brain/
├── src/
│ ├── init.py
│ └── brain.py
├── tests/
│ └── test_brain.py
├── pyproject.toml
├── requirements.txt
└── README.md


---

## Determinism & Control Guarantees

The code enforces the following guarantees:
- Stateless execution
- Fixed execution order
- No retries or branching outside defined conditions
- No randomness or time-based behavior
- Immediate termination on failure or confirmation requirement

---

## Limitations

- External modules must be provided for decomposition, safety checks, and execution
- No persistence or session handling
- No support for partial continuation after confirmation
- No dynamic configuration or extensibility

---

## Usage

This module is intended to be used as a Python library.  
The primary entry point is the `personal_ai_brain` function defined in `src/brain.py`.

---

## Status

Locked
