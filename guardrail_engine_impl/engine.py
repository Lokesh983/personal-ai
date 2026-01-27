# engine.py

class GuardrailEngine:
    def __init__(
        self,
        rule_validator,
        reasoning_layer,
        reasoning_validator,
        confirmation_evaluator,
        decision_merger,
        audit_logger,
    ):
        self.rule_validator = rule_validator
        self.reasoning_layer = reasoning_layer
        self.reasoning_validator = reasoning_validator
        self.confirmation_evaluator = confirmation_evaluator
        self.decision_merger = decision_merger
        self.audit_logger = audit_logger

    def evaluate(self, raw_input_snapshot: dict, timestamp_utc: str) -> dict:
        # 1. Rule validation
        rule_validation = self.rule_validator.validate(raw_input_snapshot)

        # 2. LLM reasoning (advisory only)
        reasoning_text = self.reasoning_layer.generate(raw_input_snapshot)

        # 3. Reasoning validation (structure only)
        reasoning_validation = self.reasoning_validator.validate(
            raw_input_snapshot["task_id"],
            reasoning_text,
        )

        # 4. Confirmation evaluation (independent)
        required_confirmation = self.confirmation_evaluator.evaluate(
            raw_input_snapshot
        )

        # 5. Decision merge (canonical output)
        final_decision = self.decision_merger.merge(
            rule_validation=rule_validation,
            reasoning_validation=reasoning_validation,
            required_confirmation=required_confirmation,
        )

        # 6. Audit logging (append-only, immutable)
        self.audit_logger.log(
            timestamp_utc=timestamp_utc,
            raw_input_snapshot=raw_input_snapshot,
            final_decision=final_decision,
            reasoning_text=reasoning_validation["model_explanation"],
        )

        return final_decision
