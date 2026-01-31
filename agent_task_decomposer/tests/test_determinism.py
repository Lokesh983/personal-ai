import json

from decomposer.decomposer import decompose
from decomposer.models import DecompositionInput


def make_input(goal_id: str, user_goal: str):
    return DecompositionInput(
        goal_id=goal_id,
        user_goal=user_goal,
        context={
            "available_tools": [],
            "workspace_paths": [],
            "constraints": [],
        },
    )


def serialize_plan(plan):
    """
    Deterministically serialize TaskPlan for byte-level comparison.
    """
    return json.dumps(
        {
            "plan_id": plan.plan_id,
            "tasks": [
                {
                    "task_id": t.task_id,
                    "task_type": t.task_type.value,
                    "task_parameters": t.task_parameters,
                    "depends_on": t.depends_on,
                }
                for t in plan.tasks
            ],
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def test_byte_identical_output():
    inp = make_input("det1", "create file /tmp/a.txt")

    plan_a = decompose(inp)
    plan_b = decompose(inp)

    serialized_a = serialize_plan(plan_a)
    serialized_b = serialize_plan(plan_b)

    assert serialized_a == serialized_b
