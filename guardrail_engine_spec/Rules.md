# Rule System Specification

## Rule Categories
- ACTION
- FILESYS
- PATH
- FILETYPE
- OPER
- CONTENT
- PERM
- RESOURCE
- CONFIRM
- SYSINTEGRITY

## Rule ID Format


Example:
- R_OPER_003
- R_SYSINTEGRITY_002

## Rule Characteristics
- Boolean evaluation only
- Order-independent
- No severity weighting
- No rule dependencies
- No rule mutation
- No reference to LLM output

## Rule Metadata Schema
```json
{
  "id": "",
  "category": "",
  "description": "",
  "severity": "",
  "applies_to": [],
  "failure_message": ""
}
