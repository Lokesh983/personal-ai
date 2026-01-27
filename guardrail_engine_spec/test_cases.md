# Use Case Tests — Personal AI Guardrail Engine (v2.0.0)

## Purpose

This document defines the **canonical, mandatory test cases** for the
Personal AI Guardrail Engine (v2).

These tests validate **behavioral correctness, determinism, and safety**
across the expanded task capabilities introduced in v2.

These tests are **normative**.
Any implementation claiming compliance with v2 **must** satisfy all cases
without deviation.

---

## Global Test Constraints (Non-Negotiable)

All test cases must satisfy the following:

- Input schema matches `raw_input_snapshot` exactly
- Only supported `task_type` values are used
- Rule validation is the **sole authority** for approval
- Reasoning validation never affects approval
- Confirmation never appears in `failed_checks`
- Output schema is canonical and frozen
- `reason` is one of exactly:
  - `"All checks passed."`
  - `"One or more rule checks failed."`
- Same input must always produce the same output

---

Test Case 1 — Clean Approval (General Task)
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_001",
  "task_type": "TEXT_SUMMARIZATION",
  "task_parameters": {
    "source": "document"
  },
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}
Rule Validator Output
{
  "passed": true,
  "failed_checks": []
}

Reasoning Validator Output
{
  "passed": true,
  "model_explanation": "The task requests summarization of a provided document."
}

Confirmation Evaluator Output
{
  "required_confirmation": false
}

Final Decision JSON
{
  "approved": true,
  "reason": "All checks passed.",
  "rule_validation": {
    "passed": true,
    "failed_checks": []
  },
  "reasoning_validation": {
    "passed": true,
    "model_explanation": "The task requests summarization of a provided document."
  },
  "required_confirmation": false,
  "safe_alternatives": []
}

Test Case 2 — Hard Rejection (Unsupported Task Type)
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_002",
  "task_type": "UNKNOWN_ACTION",
  "task_parameters": {},
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}

Rule Validator Output
{
  "passed": false,
  "failed_checks": ["R_INTEGRITY_001"]
}

Reasoning Validator Output
{
  "passed": true,
  "model_explanation": "The task specifies an unsupported action type."
}

Confirmation Evaluator Output
{
  "required_confirmation": false
}

Final Decision JSON
{
  "approved": false,
  "reason": "One or more rule checks failed.",
  "rule_validation": {
    "passed": false,
    "failed_checks": ["R_INTEGRITY_001"]
  },
  "reasoning_validation": {
    "passed": true,
    "model_explanation": "The task specifies an unsupported action type."
  },
  "required_confirmation": false,
  "safe_alternatives": []
}

Test Case 3 — Reasoning Invalid, Approval Unaffected
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_003",
  "task_type": "FILE_READ",
  "task_parameters": {
    "path": "/user/docs/report.txt"
  },
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}

Rule Validator Output
{
  "passed": true,
  "failed_checks": []
}

Reasoning Validator Output
{
  "passed": false,
  "model_explanation": "Reasoning output discarded for non-compliance."
}

Confirmation Evaluator Output
{
  "required_confirmation": false
}

Final Decision JSON
{
  "approved": true,
  "reason": "All checks passed.",
  "rule_validation": {
    "passed": true,
    "failed_checks": []
  },
  "reasoning_validation": {
    "passed": false,
    "model_explanation": "Reasoning output discarded for non-compliance."
  },
  "required_confirmation": false,
  "safe_alternatives": []
}

Test Case 4 — Confirmation Required (Filesystem Operation)
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_004",
  "task_type": "FILE_DELETE",
  "task_parameters": {
    "path": "/user/docs/archive/"
  },
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}

Rule Validator Output
{
  "passed": true,
  "failed_checks": []
}

Reasoning Validator Output
{
  "passed": true,
  "model_explanation": "The task requests deletion of a specified filesystem path."
}

Confirmation Evaluator Output
{
  "required_confirmation": true
}

Final Decision JSON
{
  "approved": true,
  "reason": "All checks passed.",
  "rule_validation": {
    "passed": true,
    "failed_checks": []
  },
  "reasoning_validation": {
    "passed": true,
    "model_explanation": "The task requests deletion of a specified filesystem path."
  },
  "required_confirmation": true,
  "safe_alternatives": []
}

Test Case 5 — Hard Rejection (System Command)
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_005",
  "task_type": "SYSTEM_COMMAND",
  "task_parameters": {
    "command": "shutdown -h now"
  },
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}

Rule Validator Output
{
  "passed": false,
  "failed_checks": ["R_SYS_COMMANDS_002"]
}

Reasoning Validator Output
{
  "passed": true,
  "model_explanation": "The task specifies execution of a system-level command."
}

Confirmation Evaluator Output
{
  "required_confirmation": false
}

Final Decision JSON
{
  "approved": false,
  "reason": "One or more rule checks failed.",
  "rule_validation": {
    "passed": false,
    "failed_checks": ["R_SYS_COMMANDS_002"]
  },
  "reasoning_validation": {
    "passed": true,
    "model_explanation": "The task specifies execution of a system-level command."
  },
  "required_confirmation": false,
  "safe_alternatives": []
}

Test Case 6 — Internet Access with Confirmation
Input (raw_input_snapshot)
{
  "task_id": "TC_V2_006",
  "task_type": "WEB_SCRAPE",
  "task_parameters": {
    "url": "https://example.com/data"
  },
  "task_source_id": "agent",
  "task_schema_version": "1.0.0"
}

Rule Validator Output
{
  "passed": true,
  "failed_checks": []
}

Reasoning Validator Output
{
  "passed": true,
  "model_explanation": "The task requests retrieval of data from a specified web resource."
}

Confirmation Evaluator Output
{
  "required_confirmation": true
}

Final Decision JSON
{
  "approved": true,
  "reason": "All checks passed.",
  "rule_validation": {
    "passed": true,
    "failed_checks": []
  },
  "reasoning_validation": {
    "passed": true,
    "model_explanation": "The task requests retrieval of data from a specified web resource."
  },
  "required_confirmation": true,
  "safe_alternatives": []
}
Compliance Statement

An implementation is compliant with Personal AI Guardrail Engine v2.0.0
if and only if all test cases in this document:

Produce the exact approval outcome

Produce the exact canonical JSON structure

Preserve determinism

Enforce confirmation correctly

Never allow unsupported task types

Never allow reasoning to influence approval

Any deviation constitutes a spec violation.