# Atomicity invariants that every task must satisfy
ATOMICITY_INVARIANTS = (
    "single_external_effect",
    "no_hidden_sequence",
    "no_cognitive_action",
    "no_compound_action",
    "no_state_inspection",
)

# Verbs and action patterns that are always non-atomic
NON_ATOMIC_VERBS = {
    "and",
    "then",
    "after",
    "before",
    "if",
    "else",
    "unless",
    "while",
    "for each",
    "loop",
    "repeat",
    "verify",
    "check",
    "confirm",
    "analyze",
    "decide",
    "determine",
    "evaluate",
    "plan",
    "think",
}

# Task types that are forbidden by definition (must never appear)
FORBIDDEN_TASK_TYPES = {
    "EXECUTE_COMMAND",
    "RUN_SCRIPT",
    "SETUP_ENVIRONMENT",
    "INSTALL_DEPENDENCIES",
    "CONFIGURE_SYSTEM",
    "VALIDATE_STATE",
    "CHECK_EXISTENCE",
    "GENERIC_ACTION",
    "CUSTOM_ACTION",
}

# Fields that must never encode logic or control flow
FORBIDDEN_PARAMETER_KEYS = {
    "if",
    "when",
    "unless",
    "condition",
    "conditions",
    "steps",
    "step",
    "sequence",
    "order",
    "logic",
}
