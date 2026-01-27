# Rule System Specification — Personal AI Guardrail Engine (v2.0.0)

## Purpose

This document defines the **rule system contract** for the Personal AI Guardrail Engine (v2).

Rules are the **sole authority** for task approval or rejection.
They are deterministic, explicit, and auditable.

This document defines **structure, categories, and constraints only**.
It does **not** define rule logic or implementations.

---

## Rule Categories (Mandatory & Frozen)

The Guardrail Engine uses **exactly eight (8)** rule categories.

No additional categories are allowed.

1. `OPERATIONS`  
2. `IO_FILESYSTEM`  
3. `IO_NETWORK`  
4. `SYS_COMMANDS`  
5. `APP_AUTOMATION`  
6. `CONFIRMATION`  
7. `INTEGRITY`  
8. `SAFETY`

Any rule must belong to **one and only one** of these categories.

---

## Rule ID Format (Strict)

All rules must use the following ID format:

# Rule System Specification — Personal AI Guardrail Engine (v2.0.0)

## Purpose

This document defines the **rule system contract** for the Personal AI Guardrail Engine (v2).

Rules are the **sole authority** for task approval or rejection.
They are deterministic, explicit, and auditable.

This document defines **structure, categories, and constraints only**.
It does **not** define rule logic or implementations.

---

## Rule Categories (Mandatory & Frozen)

The Guardrail Engine uses **exactly eight (8)** rule categories.

No additional categories are allowed.

1. `OPERATIONS`  
2. `IO_FILESYSTEM`  
3. `IO_NETWORK`  
4. `SYS_COMMANDS`  
5. `APP_AUTOMATION`  
6. `CONFIRMATION`  
7. `INTEGRITY`  
8. `SAFETY`

Any rule must belong to **one and only one** of these categories.

---

## Rule ID Format (Strict)

All rules must use the following ID format:

R_<CATEGORY>_<3-digit-number>


### Examples
- `R_IO_FILESYSTEM_003`
- `R_SYS_COMMANDS_001`
- `R_SAFETY_007`

Constraints:
- `<CATEGORY>` must match one of the eight allowed categories exactly
- `<3-digit-number>` must be zero-padded (001–999)
- Rule IDs are immutable once defined

---

## Rule Characteristics (Non-Negotiable)

All rules are:

- **Boolean** (pass or fail only)
- **Order-independent**
- **Deterministic**
- **Non-self-modifying**
- **Traceable**
- **Stateless**
- **Non-learning**

Rules must NOT:
- Assign severity levels
- Use weights or scores
- Depend on other rules
- Reference LLM output
- Infer intent or risk
- Change behavior over time

---

## Rule Evaluation Model

Rules are evaluated using a **pure boolean model**.

For each rule:
- `true` → rule passes
- `false` → rule fails

All rules are evaluated **exhaustively**.
No short-circuiting is allowed.

### Approval Logic (Authoritative)


### Examples
- `R_IO_FILESYSTEM_003`
- `R_SYS_COMMANDS_001`
- `R_SAFETY_007`

Constraints:
- `<CATEGORY>` must match one of the eight allowed categories exactly
- `<3-digit-number>` must be zero-padded (001–999)
- Rule IDs are immutable once defined

---

## Rule Characteristics (Non-Negotiable)

All rules are:

- **Boolean** (pass or fail only)
- **Order-independent**
- **Deterministic**
- **Non-self-modifying**
- **Traceable**
- **Stateless**
- **Non-learning**

Rules must NOT:
- Assign severity levels
- Use weights or scores
- Depend on other rules
- Reference LLM output
- Infer intent or risk
- Change behavior over time

---

## Rule Evaluation Model

Rules are evaluated using a **pure boolean model**.

For each rule:
- `true` → rule passes
- `false` → rule fails

All rules are evaluated **exhaustively**.
No short-circuiting is allowed.

### Approval Logic (Authoritative)

approved = (failed_checks is empty)

If **any** rule fails, the task is rejected.

---

## Confirmation Rules (Special Handling)

Rules in the `CONFIRMATION` category are **not safety failures**.

### Properties of Confirmation Rules

- They NEVER appear in `failed_checks`
- They NEVER cause rejection
- They NEVER influence `approved`
- They ONLY signal that `required_confirmation = true`

Confirmation rules represent **workflow gating**, not violations.

---

## Rule Application Scope

Rules may apply based on:

- `task_type`
- `task_parameters`
- Structural properties of the input

Rules must NOT:
- Infer user intent
- Infer semantic meaning
- Infer risk levels
- Access external systems
- Depend on execution context

---

## Supported Task Type Enforcement

Rules must enforce that **only supported task types** may be approved.

Any task whose `task_type` is not in the allowed list
must be rejected by rule evaluation.

Supported task types include:

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

---

## Rule Metadata Schema (Structural Only)

Each rule definition must conform to the following metadata schema:

```json
{
  "id": "",
  "category": "",
  "description": "",
  "applies_to": [],
  "failure_message": ""
}

Field Definitions

id
Immutable rule identifier following the required format

category
One of the eight allowed rule categories

description
Human-readable summary of the rule’s purpose

applies_to
List of task types the rule applies to

failure_message
Static, deterministic message used when the rule fails

No logic is included in this schema.

Prohibited Rule Behaviors

Rules must NEVER:

Execute tasks

Modify system or filesystem state

Access network resources

Call external APIs

Generate new rules

Modify existing rules

Reference confirmation logic outside the CONFIRMATION category

Change approval logic

Any such behavior is a spec violation.

Determinism & Audit Guarantees

Because rules are:

Boolean

Stateless

Deterministic

The following guarantees hold:

Same input → same rule outcomes

Same failed rule IDs → same approval decision

Rule failures are fully auditable

No hidden or implicit decision logic exists

Summary

The rule system in v2 enforces explicit, deterministic approval authority across an expanded set of task domains, including filesystem, system, and internet actions.

Rules do not attempt to be intelligent.
They exist to be correct, predictable, and enforceable.

Any system that bypasses or weakens these rules is operating outside the Guardrail Engine specification.