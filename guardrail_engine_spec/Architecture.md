# Architecture — Personal AI Guardrail Engine

## Execution Order (Fixed)

1. Input Receiver
2. Rule Validator
3. LLM Reasoning Layer (advisory only)
4. Reasoning Validator
5. Confirmation Evaluator
6. Decision Merger
7. Audit Logger
8. Final Output Emitter

Execution order is **non-configurable**.

---

## Component Responsibilities

### Rule Validator
- Evaluates all rules deterministically
- Produces pass/fail + failed rule IDs
- Sole authority for approval

### LLM Reasoning Layer
- Produces neutral, non-authoritative text
- Never sees rules
- Never decides approval

### Reasoning Validator
- Validates LLM output structure only
- Rejects non-compliant reasoning safely

### Confirmation Evaluator
- Independently sets `required_confirmation`
- Based only on task_type / task_parameters
- No rule involvement

### Decision Merger
- Combines outputs into canonical JSON
- No inference
- No branching

### Audit Logger
- Append-only
- Immutable
- Replay-safe

---

## Determinism Guarantees
- Same input → same output
- No randomness
- Fixed LLM temperature
- No timestamps generated internally

---

## Explicit Non-Goals
- No execution
- No intent inference
- No semantic interpretation
- No learning or evolution
- No dynamic schema
