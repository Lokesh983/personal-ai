import pytest
from brain import personal_ai_brain


# -------------------------
# Test Stubs (Deterministic)
# -------------------------

def decomposer_empty(_):
    return {"tasks": []}


def decomposer_single_task(_):
    return {
        "tasks": [
            {"task_id": "task-1", "task_payload": {}}
        ]
    }


def guardrail_reject(_):
    return {"status": "rejected", "reason": "unsafe"}


def guardrail_confirm(_):
    return {"status": "confirmation_required", "reason": "needs approval"}


def guardrail_approve(_):
    return {"status": "approved", "reason": "ok"}


def executor_fail(task):
    return {
        "task_id": task["task_id"],
        "outcome": "failure",
        "result": {}
    }


def executor_success(task):
    return {
        "task_id": task["task_id"],
        "outcome": "success",
        "result": {}
    }


# -------------------------
# Monkeypatch Helpers
# -------------------------

def inject(monkeypatch, decomposer, guardrail, executor):
    monkeypatch.setattr("brain.task_decomposer", decomposer)
    monkeypatch.setattr("brain.guardrail_engine", guardrail)
    monkeypatch.setattr("brain.action_executor", executor)


# -------------------------
# Tests
# -------------------------

def test_empty_task_list_fails(monkeypatch):
    inject(monkeypatch, decomposer_empty, guardrail_approve, executor_success)

    result = personal_ai_brain({"user_input": "do something"})

    assert result == {
        "status": "failed",
        "summary": "No tasks produced",
        "actions": []
    }


def test_guardrail_rejection_stops_execution(monkeypatch):
    inject(monkeypatch, decomposer_single_task,
           guardrail_reject, executor_success)

    result = personal_ai_brain({"user_input": "unsafe task"})

    assert result == {
        "status": "failed",
        "summary": "Task rejected by safety engine",
        "actions": []
    }


def test_confirmation_required_halts(monkeypatch):
    inject(monkeypatch, decomposer_single_task,
           guardrail_confirm, executor_success)

    result = personal_ai_brain({"user_input": "needs confirmation"})

    assert result == {
        "status": "confirmation_required",
        "summary": "User confirmation required",
        "actions": []
    }


def test_executor_failure_stops_pipeline(monkeypatch):
    inject(monkeypatch, decomposer_single_task,
           guardrail_approve, executor_fail)

    result = personal_ai_brain({"user_input": "task fails"})

    assert result == {
        "status": "failed",
        "summary": "Task execution failed",
        "actions": []
    }


def test_successful_execution(monkeypatch):
    inject(monkeypatch, decomposer_single_task,
           guardrail_approve, executor_success)

    result = personal_ai_brain({"user_input": "valid task"})

    assert result == {
        "status": "completed",
        "summary": "All tasks executed successfully",
        "actions": [
            {"task_id": "task-1", "outcome": "success"}
        ]
    }
