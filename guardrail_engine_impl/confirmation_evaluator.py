# confirmation_evaluator.py

def evaluate_confirmation(raw_input_snapshot: dict) -> bool:
    """
    Independent confirmation evaluator.
    Deterministic, rule-independent.
    """

    task_type = raw_input_snapshot.get("task_type")

    if task_type == "BULK_OPERATION":
        return True

    return False
