# reasoning_validator.py

PLACEHOLDER_TEXT = "Reasoning output discarded for non-compliance."


def validate_reasoning(task_id: str, llm_reasoning_text: str) -> dict:
    """
    Structural validation only.
    """

    if not isinstance(llm_reasoning_text, str):
        return {
            "passed": False,
            "model_explanation": PLACEHOLDER_TEXT
        }

    if len(llm_reasoning_text) > 2048:
        return {
            "passed": False,
            "model_explanation": PLACEHOLDER_TEXT
        }

    return {
        "passed": True,
        "model_explanation": llm_reasoning_text
    }
