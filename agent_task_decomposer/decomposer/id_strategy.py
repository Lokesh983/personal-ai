def derive_plan_id(goal_id: str, user_goal: str) -> str:
    """
    Deterministically derive a plan_id from goal_id and user_goal.
    """
    return f"plan::{goal_id}::{user_goal}"


def derive_task_id(plan_id: str, index: int) -> str:
    """
    Deterministically derive a task_id from plan_id and task index.
    """
    return f"{plan_id}::task::{index}"
