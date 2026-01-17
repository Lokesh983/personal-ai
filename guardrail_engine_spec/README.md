# Personal AI Guardrail Engine — Specification v1.0.0

This repository contains the **formal specification** for a deterministic Guardrail Engine
used to validate AI-generated tasks before execution.

## Purpose
The Guardrail Engine acts as a **mandatory approval layer** between task generation
(LLM or deterministic) and task execution.

It ensures:
- Deterministic validation
- Explicit rule-based enforcement
- Zero execution authority
- Full auditability
- No intent inference
- No hallucination-based decisions

## What This System Is
- A validation and approval specification
- A rule-first, reasoning-second architecture
- A non-executing, non-agentic safety layer

## What This System Is NOT
- An executor
- An agent
- A planner
- A policy model
- A learning system

## Output Contract
The engine produces **one and only one** canonical JSON decision output.
All downstream systems must obey it blindly.

## Version
This specification is frozen as **v1.0.0**.
Any changes require a formal versioning phase.
