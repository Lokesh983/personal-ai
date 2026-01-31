from core.validator import validate_input, ValidationError
from core.dispatcher import dispatch, DispatchError
from core.confirmation import is_valid_confirmation
from core.output import assemble_output
from audit_logging.audit_log import append_log_entry, LoggingError


def handle_request(payload: dict, user_confirmation: str = None):
    """
    Entry point for a single request.
    Returns either:
    - Confirmation prompt string
    - Strict output JSON
    """

    # ---- Validation gate ----
    try:
        decision = validate_input(payload)
    except ValidationError as e:
        return assemble_output(
            executed=False,
            details="",
            error=str(e),
            raw_input_snapshot=payload.get("raw_input_snapshot", {}),
            guardrail_decision=payload.get("guardrail_decision", {}),
            executor_result="",
            external_timestamp=payload.get("external_timestamp", ""),
        )

    # ---- Confirmation pause ----
    if decision == "PAUSE":
        if not is_valid_confirmation(user_confirmation or ""):
            return "Confirmation required. Reply YES to proceed."

    raw_task = payload["raw_input_snapshot"]
    guardrail = payload["guardrail_decision"]
    timestamp = payload["external_timestamp"]

    # ---- Dispatch ----
    try:
        action, executor = dispatch(raw_task, guardrail)
        if action == "PAUSE":
            return "Confirmation required. Reply YES to proceed."
    except DispatchError as e:
        return assemble_output(
            executed=False,
            details="",
            error=str(e),
            raw_input_snapshot=raw_task,
            guardrail_decision=guardrail,
            executor_result="",
            external_timestamp=timestamp,
        )

    # ---- Execute exactly one action ----
    try:
        result = executor(raw_task)
        executor_result = "Action executed successfully"
        details = "Execution completed"
        executed = True
        error = ""
    except Exception as e:
        executor_result = ""
        details = ""
        executed = False
        error = str(e)

    # ---- Log (append-only) ----
    log_entry = {
        "raw_input_snapshot": raw_task,
        "guardrail_decision": guardrail,
        "executor_result": executor_result,
        "external_timestamp": timestamp,
    }

    try:
        append_log_entry(log_entry)
    except LoggingError as e:
        return assemble_output(
            executed=False,
            details="",
            error=str(e),
            raw_input_snapshot=raw_task,
            guardrail_decision=guardrail,
            executor_result="",
            external_timestamp=timestamp,
        )

    # ---- Final output ----
    return assemble_output(
        executed=executed,
        details=details,
        error=error,
        raw_input_snapshot=raw_task,
        guardrail_decision=guardrail,
        executor_result=executor_result,
        external_timestamp=timestamp,
    )
