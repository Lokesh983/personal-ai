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


def test_compound_action_rejected():
    inp = make_input(
        "atom1",
        "write hello and then save to file /tmp/a.txt",
    )

    plan = decompose(inp)

    assert plan.tasks == []


def test_cognitive_action_rejected():
    inp = make_input(
        "atom2",
        "decide where to create file /tmp/a.txt",
    )

    plan = decompose(inp)

    assert plan.tasks == []
