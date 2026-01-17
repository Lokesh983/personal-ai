# Use Case Tests — Personal AI Guardrail Engine

This document defines the **canonical use case tests** for the Guardrail Engine
specification v1.0.0.

These tests validate **contract correctness**, not implementation details.

---

## Purpose of These Tests

The test cases exist to ensure that:

- The canonical input schema is respected
- The canonical output schema is enforced
- Rule validation remains the sole approval authority
- Reasoning validation never affects approval
- Confirmation handling is orthogonal to rule validation
- Deterministic behavior is preserved across runs

These tests are **normative**.

Any implementation claiming compliance with this specification
**must produce identical outputs** for the same inputs.

---

## Covered Scenarios

The following scenarios are explicitly covered and required:

### 1. Clean Approval
- All rules pass
- Reasoning output is valid
- Confirmation is not required
- Approval is granted

### 2. Hard Rejection (Rule Failure)
- One or more rules fail
- Approval is denied
- Reasoning output does not override rejection
- Confirmation is not applicable

### 3. Reasoning Invalid, Approval Unaffected
- All rules pass
- LLM reasoning fails structural validation
- Reasoning is replaced with deterministic placeholder
- Approval remains granted

### 4. Confirmation Required
- All rules pass
- Confirmation evaluator sets `required_confirmation = true`
- Approval remains granted
- Confirmation does not appear as a rule failure

### 5. Multiple Rule Failures
- More than one rule fails
- All failed rule IDs are reported
- Approval is denied
- Reasoning output remains advisory only

---

## Mandatory Constraints

All test cases must satisfy the following:

- Inputs must match the canonical `raw_input_snapshot` schema
- Outputs must match the canonical decision JSON schema
- `approved` must depend **only** on rule validation
- `reason` must be one of exactly two allowed values:
  - `"All checks passed."`
  - `"One or more rule checks failed."`
- Reasoning failures must never block approval
- Confirmation must never appear in `failed_checks`
- No inferred intent or contextual assumptions are allowed

---

## Non-Goals of These Tests

These tests do **not**:

- Define rule logic
- Define execution behavior
- Define UI behavior
- Optimize performance
- Allow schema extensions

They exist solely to enforce **behavioral correctness and determinism**.

---

## Compliance Statement

An implementation is considered **compliant with Guardrail Engine v1.0.0**
if and only if it passes all test scenarios described in this document
without deviation.

Any deviation constitutes a **spec violation**.
