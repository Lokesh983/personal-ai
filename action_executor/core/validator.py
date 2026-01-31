from constants.task_types import ALLOWED_TASK_TYPES


class ValidationError(Exception):
    pass


def validate_input(payload: dict) -> str:
    """
    Returns one of: 'PASS', 'PAUSE'
    Raises ValidationError on hard failure
    """

    # ---- 1. Top-level structure ----
    required_top_fields = {
        "raw_input_snapshot",
        "guardrail_decision",
        "external_timestamp"
    }

    if set(payload.keys()) != required_top_fields:
        raise ValidationError("Invalid input envelope. Execution aborted.")

    raw_task = payload["raw_input_snapshot"]
    guardrail = payload["guardrail_decision"]
    timestamp = payload["external_timestamp"]

    # ---- 2. External timestamp ----
    if not isinstance(timestamp, str) or not timestamp.strip():
        raise ValidationError("Missing or invalid external timestamp.")

    # ---- 3. Task schema validation ----
    required_task_fields = {
        "task_id",
        "task_type",
        "task_parameters",
        "task_source_id",
        "task_schema_version"
    }

    if set(raw_task.keys()) != required_task_fields:
        raise ValidationError("Invalid task schema. Execution aborted.")

    if raw_task["task_schema_version"] != "1.0.0":
        raise ValidationError("Invalid task schema version.")

    task_type = raw_task["task_type"]
    task_params = raw_task["task_parameters"]

    if task_type not in ALLOWED_TASK_TYPES:
        raise ValidationError("Unsupported task type.")

    if not isinstance(task_params, dict):
        raise ValidationError("task_parameters must be an object.")

    # ---- 4. Guardrail decision validation ----
    required_guardrail_fields = {"approved", "required_confirmation"}

    if not required_guardrail_fields.issubset(guardrail.keys()):
        raise ValidationError("Guardrail decision invalid.")

    if guardrail["approved"] is False:
        raise ValidationError(
            "Action not executed. Guardrail rejected the task.")

    # ---- 5. Confirmation gate ----
    if guardrail.get("required_confirmation") is True:
        return "PAUSE"

    return "PASS"
