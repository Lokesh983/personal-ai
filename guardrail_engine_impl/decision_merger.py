# decision_merger.py

def merge_decision(
    rule_validation: dict,
    reasoning_validation: dict,
    required_confirmation: bool
) -> dict:

    approved = rule_validation["passed"]

    reason = (
        "All checks passed."
        if approved
        else "One or more rule checks failed."
    )

    return {
        "approved": approved,
        "reason": reason,
        "rule_validation": rule_validation,
        "reasoning_validation": reasoning_validation,
        "required_confirmation": required_confirmation,
        "safe_alternatives": []
    }
