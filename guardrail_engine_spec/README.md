# Personal AI Guardrail Engine — Specification v2.0.0

## Overview

The **Personal AI Guardrail Engine (v2)** is a deterministic, rule-first validation system
that evaluates **AI-generated tasks** before they are allowed to reach any execution layer.

This engine acts as a **mandatory approval authority** between:
- AI agents that generate tasks, and
- downstream systems that may execute those tasks.

The engine itself **never executes anything**.

---

## Why This Project Exists

Modern AI systems increasingly generate **actions**, not just text.
These actions may involve:

- Filesystem operations
- System commands
- Application automation
- Internet access
- API calls
- Downloads
- Bulk operations

LLMs are **probabilistic** and **hallucination-prone**.
Allowing them to directly authorize actions introduces unacceptable risk.

This project exists to ensure that:

- AI models **cannot approve their own outputs**
- All decisions are **deterministic and reproducible**
- Safety is enforced through **explicit rules**, not inference
- Execution systems are **never responsible for safety decisions**

---

## Core Philosophy

The Guardrail Engine is built on the following principles:

- **Rule-first, reasoning-second**
- **Zero inference**
- **Zero hallucinated authority**
- **Determinism over intelligence**
- **Validation ≠ execution**

The engine is intentionally **boring**.
Predictability and auditability are higher priorities than flexibility.

---

## What the Engine DOES

The Guardrail Engine WILL:

- Validate AI-generated tasks
- Approve or reject tasks using deterministic rules
- Enforce confirmation for sensitive actions
- Produce exactly one canonical decision JSON
- Generate advisory (non-authoritative) LLM reasoning
- Log decisions immutably for audit and replay

---

## What the Engine DOES NOT Do

The Guardrail Engine WILL NOT:

- Execute tasks
- Modify files or system state
- Access the filesystem or network
- Interpret user intent
- Infer risk or semantic meaning
- Use randomness or temperature > 0
- Learn, adapt, or evolve rules
- Allow models to self-validate correctness

Any system performing these actions is **outside the scope** of this engine.

---

## Supported Task Types (v2)

The engine may validate **only** the following task types.

### General
- `TEXT_SUMMARIZATION`
- `BULK_OPERATION`

### Filesystem
- `FILE_READ`
- `FILE_WRITE`
- `FILE_DELETE`
- `FOLDER_CREATE`

### System
- `SYSTEM_COMMAND`
- `RUN_TOOL`
- `APPLICATION_OPEN`

### Internet
- `INTERNET_SEARCH`
- `WEB_SCRAPE`
- `API_REQUEST`

### Download
- `DOWNLOAD_FILE`

Any task type **not in this list must be rejected**.

---

## Output Contract

The engine always produces the **same canonical JSON structure**:

```json
{
  "approved": false,
  "reason": "",
  "rule_validation": {
    "passed": false,
    "failed_checks": []
  },
  "reasoning_validation": {
    "passed": false,
    "model_explanation": ""
  },
  "required_confirmation": false,
  "safe_alternatives": []
}
