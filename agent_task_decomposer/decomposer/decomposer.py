from typing import List
import re
import os

from .models import DecompositionInput, AtomicTask, TaskPlan
from .task_types import TaskType
from .id_strategy import derive_plan_id, derive_task_id
from .validator import validate_atomic_task


def _extract_quoted_values(text: str):
    """Return quoted substrings deterministically."""
    return re.findall(r'"([^"]+)"', text)


def _is_valid_path(path: str) -> bool:
    """Basic safety validation for empty and traversal paths."""
    if not path or path.strip() == "":
        return False

    normalized = os.path.normpath(path)

    # prevent path traversal outside workspace
    if normalized.startswith(".."):
        return False

    return True


def decompose(input_data: DecompositionInput) -> TaskPlan:
    """
    Deterministically decompose a high-level user goal into atomic tasks.
    If decomposition is not possible under v1 rules, return an empty task list.
    """

    plan_id = derive_plan_id(input_data.goal_id, input_data.user_goal)

    original_goal = input_data.user_goal.strip()
    normalized_goal = original_goal.lower()

    tasks: List[AtomicTask] = []

    # -----------------------------
    # Pattern 1: CREATE FILE + CONTENT
    # create a file "name.ext" with "content"
    # -----------------------------
    if normalized_goal.startswith("create a file"):
        values = _extract_quoted_values(original_goal)

        if len(values) >= 1:
            file_path = values[0]

            if not _is_valid_path(file_path):
                return TaskPlan(plan_id=plan_id, tasks=[])

            create_task = AtomicTask(
                task_id="",
                task_type=TaskType.CREATE_FILE,
                task_parameters={"path": file_path},
                depends_on=[],
            )
            tasks.append(create_task)

            if len(values) >= 2:
                content = values[1]

                write_task = AtomicTask(
                    task_id="",
                    task_type=TaskType.WRITE_FILE,
                    task_parameters={"path": file_path, "content": content},
                    depends_on=[],  # assigned after IDs generated
                )
                tasks.append(write_task)

    # -----------------------------
    # Pattern 2: CREATE FOLDER
    # create folder "folder name"
    # -----------------------------
    elif normalized_goal.startswith("create folder"):
        values = _extract_quoted_values(original_goal)

        if len(values) == 1:
            folder_path = values[0]

            if not _is_valid_path(folder_path):
                return TaskPlan(plan_id=plan_id, tasks=[])

            tasks.append(
                AtomicTask(
                    task_id="",
                    task_type=TaskType.CREATE_DIRECTORY,
                    task_parameters={"path": folder_path},
                    depends_on=[],
                )
            )

    # -----------------------------
    # Pattern 3: OPEN APPLICATION
    # open "app name"
    # -----------------------------
    elif normalized_goal.startswith("open"):
        values = _extract_quoted_values(original_goal)

        if len(values) == 1:
            app_name = values[0]

            tasks.append(
                AtomicTask(
                    task_id="",
                    task_type=TaskType.OPEN_APPLICATION,
                    task_parameters={"app_name": app_name},
                    depends_on=[],
                )
            )

    # -----------------------------
    # Pattern 4: SUMMARIZE FILE
    # summarize file "filename"
    # -----------------------------
    elif normalized_goal.startswith("summarize file"):
        values = _extract_quoted_values(original_goal)

        if len(values) == 1:
            file_path = values[0]

            if not _is_valid_path(file_path):
                return TaskPlan(plan_id=plan_id, tasks=[])

            tasks.append(
                AtomicTask(
                    task_id="",
                    task_type=TaskType.RECEIVE_NETWORK_RESOURCE,  # placeholder semantic action
                    task_parameters={"path": file_path,
                                     "operation": "summarize"},
                    depends_on=[],
                )
            )

    else:
        return TaskPlan(plan_id=plan_id, tasks=[])

    # -----------------------------
    # Assign deterministic IDs
    # -----------------------------
    for index, task in enumerate(tasks):
        task.task_id = derive_task_id(plan_id, index)

    # -----------------------------
    # Fix dependencies using task IDs
    # -----------------------------
    if len(tasks) == 2 and tasks[1].task_type == TaskType.WRITE_FILE:
        tasks[1].depends_on = [tasks[0].task_id]

    # -----------------------------
    # Validate tasks atomically
    # -----------------------------
    for task in tasks:
        if not validate_atomic_task(task):
            return TaskPlan(plan_id=plan_id, tasks=[])

    return TaskPlan(plan_id=plan_id, tasks=tasks)
