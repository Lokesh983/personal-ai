from typing import Any

from decomposer.task_types import TaskType
from decomposer.atomicity_rules import (
    ATOMICITY_INVARIANTS,
    NON_ATOMIC_VERBS,
    FORBIDDEN_TASK_TYPES,
    FORBIDDEN_PARAMETER_KEYS,
)
from decomposer.models import AtomicTask


def validate_atomic_task(task: AtomicTask) -> bool:
    # Rule 1 — Schema integrity
    if not isinstance(task.task_id, str):
        return False
    if not isinstance(task.task_type, TaskType):
        return False
    if not isinstance(task.task_parameters, dict):
        return False
    if not isinstance(task.depends_on, list):
        return False

    # Rule 2 — Task type validity
    if task.task_type.name in FORBIDDEN_TASK_TYPES:
        return False

    # Rule 3 — Parameter purity
    for key, value in task.task_parameters.items():
        if not isinstance(key, str):
            return False

        lower_key = key.lower()
        if lower_key in FORBIDDEN_PARAMETER_KEYS:
            return False

        if isinstance(value, str):
            lower_value = value.lower()
            for verb in NON_ATOMIC_VERBS:
                if verb in lower_value:
                    return False

    # Rule 4 — Dependency hygiene
    for dep in task.depends_on:
        if not isinstance(dep, str):
            return False

    # If all checks pass, task is atomic
    return True
