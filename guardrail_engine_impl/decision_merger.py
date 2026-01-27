# decision_merger.py

class DecisionMerger:
    def merge(
        self,
        rule_validation: dict,
        reasoning_validation: dict,
        required_confirmation: bool,
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
            "rule_validation": {
                "passed": rule_validation["passed"],
                "failed_checks": rule_validation["failed_checks"],
            },
            "reasoning_validation": {
                "passed": reasoning_validation["passed"],
                "model_explanation": reasoning_validation["model_explanation"],
            },
            "required_confirmation": required_confirmation,
            "safe_alternatives": [],
        }
