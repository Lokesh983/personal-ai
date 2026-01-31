from typing import List

from decomposer.models import DecompositionInput, AtomicTask, TaskPlan
from decomposer.task_types import TaskType
from decomposer.id_strategy import derive_plan_id, derive_task_id
from decomposer.validator import validate_atomic_task


def decompose(input_data: DecompositionInput) -> TaskPlan:
    """
    Deterministically decompose a high-level user goal into atomic tasks.
    If decomposition is not possible under v1 rules, return an empty task list.
    """

    plan_id = derive_plan_id(input_data.goal_id, input_data.user_goal)

    # Normalize goal deterministically
    goal = input_data.user_goal.strip().lower()

    tasks: List[AtomicTask] = []

    # ---- Pattern 1: CREATE_FILE ----
    if goal.startswith("create file "):
        path = goal.replace("create file ", "", 1).strip()

        tasks.append(
            AtomicTask(
                task_id="",  # assigned later
                task_type=TaskType.CREATE_FILE,
                task_parameters={"path": path},
                depends_on=[],
            )
        )

    # ---- Pattern 2: WRITE_FILE ----
    elif goal.startswith("write ") and " to file " in goal:
        content_part, file_part = goal.split(" to file ", 1)
        content = content_part.replace("write ", "", 1).strip()
        path = file_part.strip()

        tasks.append(
            AtomicTask(
                task_id="",
                task_type=TaskType.WRITE_FILE,
                task_parameters={"path": path, "content": content},
                depends_on=[],
            )
        )

    # ---- Pattern 3: CREATE_DIRECTORY ----
    elif goal.startswith("create directory "):
        path = goal.replace("create directory ", "", 1).strip()

        tasks.append(
            AtomicTask(
                task_id="",
                task_type=TaskType.CREATE_DIRECTORY,
                task_parameters={"path": path},
                depends_on=[],
            )
        )

    # ---- Unsupported goal → silent failure ----
    else:
        return TaskPlan(plan_id=plan_id, tasks=[])

    # Assign deterministic task IDs
    for index, task in enumerate(tasks):
        task.task_id = derive_task_id(plan_id, index)

    # Validate all tasks atomically
    for task in tasks:
        if not validate_atomic_task(task):
            return TaskPlan(plan_id=plan_id, tasks=[])

    return TaskPlan(plan_id=plan_id, tasks=tasks)
