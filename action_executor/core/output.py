def assemble_output(
    executed: bool,
    details: str,
    error: str,
    raw_input_snapshot: dict,
    guardrail_decision: dict,
    executor_result: str,
    external_timestamp: str,
) -> dict:
    """
    Assemble the strict executor output schema.
    """
    return {
        "executed": executed,
        "details": details,
        "error": error,
        "log_entry": {
            "raw_input_snapshot": raw_input_snapshot,
            "guardrail_decision": guardrail_decision,
            "executor_result": executor_result,
            "external_timestamp": external_timestamp,
        },
    }
