# Architecture — Personal AI Guardrail Engine (v2.0.0)

## Architectural Role

The Personal AI Guardrail Engine is a **pure validation system**.
It exists solely to decide whether an **AI-generated task** is permitted
to proceed to an execution layer.

The engine itself **never executes tasks**, never mutates state,
and never interacts with external systems.

It acts as a **central approval authority** in the AI system pipeline.

---

## High-Level Placement

In all systems that use this engine, the placement is fixed:
AI Agent / Planner
↓
Guardrail Engine (v2)
↓
Executor / Tooling Layer

No component may bypass the Guardrail Engine.
Execution systems must obey its output blindly.

---

## Fixed Component Order (Non-Negotiable)

All inputs are processed in the following order.
This order is **mandatory and non-configurable**.

1. Rule Validator  
2. LLM Reasoning Layer  
3. Reasoning Validator  
4. Confirmation Evaluator  
5. Decision Merger  
6. Audit Logger  

Any deviation from this order is a **spec violation**.

---

## Component Responsibilities

### 1. Rule Validator

**Purpose**

The Rule Validator is the **sole authority** for task approval.

**Responsibilities**

- Evaluate deterministic, boolean rules
- Collect all failed rule IDs
- Determine pass/fail based only on rule results

**Key Properties**

- Rules are order-independent
- No severity, weighting, or scoring
- No rule dependencies
- No soft failures

**Approval Logic**


No component may bypass the Guardrail Engine.
Execution systems must obey its output blindly.

---

## Fixed Component Order (Non-Negotiable)

All inputs are processed in the following order.
This order is **mandatory and non-configurable**.

1. Rule Validator  
2. LLM Reasoning Layer  
3. Reasoning Validator  
4. Confirmation Evaluator  
5. Decision Merger  
6. Audit Logger  

Any deviation from this order is a **spec violation**.

---

## Component Responsibilities

### 1. Rule Validator

**Purpose**

The Rule Validator is the **sole authority** for task approval.

**Responsibilities**

- Evaluate deterministic, boolean rules
- Collect all failed rule IDs
- Determine pass/fail based only on rule results

**Key Properties**

- Rules are order-independent
- No severity, weighting, or scoring
- No rule dependencies
- No soft failures

**Approval Logic**

passed = (failed_checks is empty)

If any rule fails, the task is rejected.

Confirmation rules never appear in `failed_checks`.

---

### 2. LLM Reasoning Layer

**Purpose**

Provide a **neutral, factual restatement** of the task metadata
for human transparency only.

**Responsibilities**

- Generate a single neutral sentence
- Restate task metadata without interpretation

**Restrictions**

The LLM must NOT:
- Approve or reject tasks
- Infer intent or risk
- Mention confirmation
- Reference rules
- Access system or internet

The LLM is **non-authoritative**.
Its output may be safely discarded.

---

### 3. Reasoning Validator

**Purpose**

Contain hallucinations and enforce strict output discipline
on the LLM reasoning text.

**Responsibilities**

- Validate structure only
- Enforce length and character constraints
- Reject forbidden phrases
- Ensure neutrality

**Behavior**

If validation fails:
- `passed = false`
- `model_explanation = "Reasoning output discarded for non-compliance."`

Reasoning validity **never affects approval**.

---

### 4. Confirmation Evaluator

**Purpose**

Determine whether a task requires explicit user confirmation
before execution.

**Responsibilities**

- Set `required_confirmation = true/false`
- Use deterministic logic only

**Constraints**

- Independent of rule validation
- Based only on `task_type` and `task_parameters`
- Never affects approval
- Never produces rule failures

Confirmation is a **workflow gate**, not a safety violation.

---

### 5. Decision Merger

**Purpose**

Assemble the final canonical decision JSON.

**Responsibilities**

- Set `approved` based only on rule validation
- Set `reason` using allowed static strings
- Merge rule validation results
- Merge reasoning validation results
- Merge confirmation result

**Constraints**

- No inference
- No branching logic
- No schema variation

---

### 6. Audit Logger

**Purpose**

Ensure every decision is auditable and replayable.

**Responsibilities**

- Record raw input snapshot
- Record final decision JSON
- Record reasoning text (validated or placeholder)
- Attach externally injected timestamp

**Constraints**

- Append-only
- Immutable
- No modification or deletion
- No internally generated timestamps

---

## Determinism Guarantees

The architecture enforces determinism through:

- Boolean rule evaluation
- Fixed component order
- No randomness
- Fixed LLM temperature (0)
- No internal time generation
- No shared mutable state

Same input always produces the same output.

---

## Validation vs Execution Boundary

A strict boundary exists between validation and execution.

The Guardrail Engine:
- Decides **whether** a task may proceed

Execution systems:
- Decide **how** to perform an approved task

Execution systems must not:
- Re-evaluate safety
- Override approval decisions
- Infer missing context
- Modify tasks to bypass validation

---

## Architectural Non-Goals

This architecture explicitly excludes:

- Task execution
- System calls
- File or network access
- Policy inference
- Learning or adaptation
- Agent autonomy
- Context accumulation

Any system performing these functions must exist
**outside** the Guardrail Engine.

---

## Summary

The Personal AI Guardrail Engine (v2) architecture enforces a
clear separation between **decision authority** and **action execution**.

By making approval deterministic, explicit, and auditable,
the engine enables safe scaling to high-risk task domains
such as filesystem access, system commands, and internet operations
without trusting AI models with authority.

The architecture is intentionally strict, explicit, and limited.
