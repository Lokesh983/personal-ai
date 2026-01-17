# engine.py
# Conforms to Guardrail Engine Spec v1.0.0

from rule_validator import validate_rules
from reasoning_layer import generate_reasoning
from reasoning_validator import validate_reasoning
from confirmation_evaluator import evaluate_confirmation
from decision_merger import merge_decision
from audit_logger import log_decision


def evaluate_task(raw_input_snapshot: dict) -> dict:
    """
    Entry point for guardrail evaluation.
    """

    # 1. Rule validation
    rule_validation = validate_rules(raw_input_snapshot)

    # 2. LLM reasoning (advisory only)
    llm_reasoning_text = generate_reasoning(
        raw_input_snapshot,
        rule_validation
    )

    # 3. Reasoning validation
    reasoning_validation = validate_reasoning(
        raw_input_snapshot["task_id"],
        llm_reasoning_text
    )

    # 4. Confirmation evaluation (independent)
    required_confirmation = evaluate_confirmation(raw_input_snapshot)

    # 5. Decision merge
    final_decision = merge_decision(
        rule_validation,
        reasoning_validation,
        required_confirmation
    )

    # 6. Audit logging (append-only)
    log_decision(raw_input_snapshot, final_decision)

    return final_decision
