class ConfirmationError(Exception):
    pass


def confirmation_required(task_type: str, guardrail_decision: dict) -> bool:
    """
    Returns True if execution must pause for user confirmation.
    """

    if not isinstance(guardrail_decision, dict):
        raise ConfirmationError("Invalid guardrail decision.")

    return guardrail_decision.get("required_confirmation") is True


def is_valid_confirmation(user_input: str) -> bool:
    """
    Only exact, uppercase YES is accepted.
    """
    return user_input == "YES"
