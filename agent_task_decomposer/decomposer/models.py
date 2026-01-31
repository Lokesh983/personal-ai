from typing import List, Dict, Any


class DecompositionInput:
    def __init__(
        self,
        goal_id: str,
        user_goal: str,
        context: Dict[str, Any],
    ):
        self.goal_id = goal_id
        self.user_goal = user_goal
        self.context = context


class AtomicTask:
    def __init__(
        self,
        task_id: str,
        task_type: str,
        task_parameters: Dict[str, Any],
        depends_on: List[str],
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.task_parameters = task_parameters
        self.depends_on = depends_on


class TaskPlan:
    def __init__(
        self,
        plan_id: str,
        tasks: List[AtomicTask],
    ):
        self.plan_id = plan_id
        self.tasks = tasks
