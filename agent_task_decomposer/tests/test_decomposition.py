from decomposer.decomposer import decompose
from decomposer.models import DecompositionInput
from decomposer.task_types import TaskType


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


def test_determinism():
    inp = make_input("g1", "create file /tmp/a.txt")

    plan_1 = decompose(inp)
    plan_2 = decompose(inp)

    assert plan_1.plan_id == plan_2.plan_id
    assert len(plan_1.tasks) == len(plan_2.tasks)

    for t1, t2 in zip(plan_1.tasks, plan_2.tasks):
        assert t1.task_id == t2.task_id
        assert t1.task_type == t2.task_type
        assert t1.task_parameters == t2.task_parameters
        assert t1.depends_on == t2.depends_on


def test_create_file_decomposition():
    inp = make_input("g2", "create file /tmp/a.txt")

    plan = decompose(inp)

    assert plan.plan_id.startswith("plan::g2")
    assert len(plan.tasks) == 1

    task = plan.tasks[0]
    assert task.task_type == TaskType.CREATE_FILE
    assert task.task_parameters == {"path": "/tmp/a.txt"}
    assert task.depends_on == []


def test_write_file_decomposition():
    inp = make_input("g3", "write hello to file /tmp/a.txt")

    plan = decompose(inp)

    assert len(plan.tasks) == 1

    task = plan.tasks[0]
    assert task.task_type == TaskType.WRITE_FILE
    assert task.task_parameters == {
        "path": "/tmp/a.txt",
        "content": "hello",
    }


def test_silent_failure_for_unsupported_goal():
    inp = make_input("g4", "delete all files in tmp")

    plan = decompose(inp)

    assert plan.plan_id.startswith("plan::g4")
    assert plan.tasks == []


def test_atomicity_gate_rejects_compound_goal():
    inp = make_input(
        "g5",
        "write hello and then save to file /tmp/a.txt",
    )

    plan = decompose(inp)

    assert plan.tasks == []
