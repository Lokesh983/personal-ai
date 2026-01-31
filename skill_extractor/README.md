# Skill Extraction Engine

A deterministic, zero-hallucination skill extraction engine designed as a reusable core module for downstream AI systems.

---

## Overview

This project implements a **strict, evidence-only skill extraction pipeline**.  
It extracts **only explicitly written skills** from arbitrary text and outputs them in a **fixed, machine-readable JSON schema**.

The system is **not generative**, **not inferential**, and **not creative**.

If a skill is not explicitly present in the input text, it is **not extracted**.

---

## Design Principles

- **Zero hallucinations**
- **No inference or interpretation**
- **Deterministic output**
- **Auditable behavior**
- **Document-agnostic**
- **Reusable as a library module**

This engine is intended to serve as a **ground-truth provider** for downstream systems such as guardrails, workflow builders, and agent planners.

---

## What This Engine Does

- Accepts arbitrary plain text (resume, job description, blog, notes, transcript, etc.)
- Cleans and preprocesses text without altering meaning
- Splits text into structure-safe chunks
- Uses embeddings **only for retrieval**, not reasoning
- Extracts skills using **strict, verbatim pattern matching**
- Normalizes and de-duplicates extracted skills using a whitelist
- Produces a fixed JSON output schema

---

## What This Engine Does NOT Do

- ❌ Infer implied skills  
- ❌ Expand abbreviations unless explicitly defined  
- ❌ Perform semantic understanding  
- ❌ Recommend skills  
- ❌ Summarize or rewrite text  
- ❌ Classify document type  
- ❌ Use LLMs for extraction decisions  

---

## Output Schema (Guaranteed)

Every execution returns **exactly** this structure:

```json
{
  "technical_skills": [],
  "soft_skills": [],
  "tools_and_technologies": [],
  "domain_knowledge": [],
  "certifications": [],
  "role_specific_skills": [],
  "other_skills": []
}
