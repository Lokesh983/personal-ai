# reasoning_validator.py

import re


class ReasoningValidator:
    MAX_LENGTH = 512

    FORBIDDEN_PATTERNS = [
        r"\{", r"\}", r"\[", r"\]",
        r"```", r"`",
        r"\bapproved\b", r"\brejected\b",
        r"\ballowed\b", r"\bblocked\b",
        r"\bsafe\b", r"\bunsafe\b",
        r"\bconfirm\b", r"\bconfirmation\b",
        r"\brule\b",
        r";", r"\|", r"&&",
    ]

    PLACEHOLDER_TEXT = "Reasoning output discarded for non-compliance."

    def validate(self, task_id: str, llm_reasoning_text: str) -> dict:
        # --- Type checks ---
        if not isinstance(task_id, str) or not task_id:
            return self._reject()

        if not isinstance(llm_reasoning_text, str):
            return self._reject()

        # --- Length check ---
        if len(llm_reasoning_text) > self.MAX_LENGTH:
            return self._reject()

        # --- Single sentence check ---
        sentence_count = llm_reasoning_text.count(".")
        if sentence_count > 1:
            return self._reject()

        # --- Forbidden pattern checks ---
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, llm_reasoning_text, re.IGNORECASE):
                return self._reject()

        return {
            "passed": True,
            "model_explanation": llm_reasoning_text,
        }

    def _reject(self) -> dict:
        return {
            "passed": False,
            "model_explanation": self.PLACEHOLDER_TEXT,
        }
