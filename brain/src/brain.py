from typing import TypedDict, List, Literal, Dict, Any
from agent_task_decomposer.decomposer.decomposer import decompose
from agent_task_decomposer.decomposer.models import DecompositionInput, TaskPlan

# =========================
# Schema Definitions
# =========================


class BrainInput(TypedDict):
    user_input: str


class WrappedInput(TypedDict):
    raw_input: str


class Task(TypedDict):
    task_id: str
    task_payload: Dict[str, Any]


class DecomposerOutput(TypedDict):
    tasks: List[Task]


GuardrailStatus = Literal[
    "approved",
    "rejected",
    "confirmation_required"
]


class GuardrailOutput(TypedDict):
    status: GuardrailStatus
    reason: str


ExecutorOutcome = Literal["success", "failure"]


class ExecutorOutput(TypedDict):
    task_id: str
    outcome: ExecutorOutcome
    result: Dict[str, Any]


FinalStatus = Literal[
    "completed",
    "failed",
    "confirmation_required"
]


class ExecutedAction(TypedDict):
    task_id: str
    outcome: ExecutorOutcome


class BrainOutput(TypedDict):
    status: FinalStatus
    summary: str
    actions: List[ExecutedAction]


# =========================
# External Module Contracts
# (Injected / Imported at Runtime)
# =========================

def task_decomposer(input_data: WrappedInput) -> DecomposerOutput:
    raise NotImplementedError


def guardrail_engine(task: Task) -> GuardrailOutput:
    raise NotImplementedError


def action_executor(task: Task) -> ExecutorOutput:
    raise NotImplementedError


# =========================
# Core Orchestrator
# =========================

def personal_ai_brain(input_data: BrainInput) -> BrainOutput:
    # Step 1: Input normalization (mechanical only)
    if "user_input" not in input_data:
        return {
            "status": "failed",
            "summary": "Input normalization failed",
            "actions": []
        }

    wrapped_input: WrappedInput = {
        "raw_input": input_data["user_input"].strip()
    }

    # Step 2: Task decomposition
    decomposed = task_decomposer(wrapped_input)

    if not decomposed.get("tasks"):
        return {
            "status": "failed",
            "summary": "No tasks produced",
            "actions": []
        }

    executed_actions: List[ExecutedAction] = []

    # Step 3: Per-task processing (strict order)
    for task in decomposed["tasks"]:
        guardrail_result = guardrail_engine(task)

        if guardrail_result["status"] == "rejected":
            return {
                "status": "failed",
                "summary": "Task rejected by safety engine",
                "actions": executed_actions
            }

        if guardrail_result["status"] == "confirmation_required":
            return {
                "status": "confirmation_required",
                "summary": "User confirmation required",
                "actions": executed_actions
            }

        execution_result = action_executor(task)

        if execution_result["outcome"] == "failure":
            return {
                "status": "failed",
                "summary": "Task execution failed",
                "actions": executed_actions
            }

        executed_actions.append({
            "task_id": execution_result["task_id"],
            "outcome": execution_result["outcome"]
        })

    # Step 4: Final output
    return {
        "status": "completed",
        "summary": "All tasks executed successfully",
        "actions": executed_actions
    }


def run_brain(input_data: dict) -> BrainOutput:
    if "user_input" not in input_data:
        return {
            "status": "failed",
            "summary": "Missing user_input",
            "actions": []
        }

    return personal_ai_brain({
        "user_input": input_data["user_input"]
    })


class PersonalAIBrain:
    def __init__(self):
        self.decomposer = _TaskDecomposerAdapter()

    def process_request(self, user_input: str):
        decomposition_input = DecompositionInput(
            goal_id="cli-request",
            user_goal=user_input,
            context={},
        )
        task_plan = self.decomposer.decompose(decomposition_input)
        return self._serialize_task_plan(task_plan)

    @staticmethod
    def _serialize_task_plan(task_plan: TaskPlan) -> Dict[str, Any]:
        return {
            "plan_id": task_plan.plan_id,
            "tasks": [
                {
                    "task_id": task.task_id,
                    "task_type": getattr(task.task_type, "value", str(task.task_type)),
                    "task_parameters": task.task_parameters,
                    "depends_on": task.depends_on,
                }
                for task in task_plan.tasks
            ],
        }


class _TaskDecomposerAdapter:
    def decompose(self, input_data: DecompositionInput) -> TaskPlan:
        return decompose(input_data)
