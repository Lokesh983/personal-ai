class GeneralError(Exception):
    pass


def general_executor(task: dict) -> dict:
    task_type = task["task_type"]
    params = task["task_parameters"]

    if task_type == "TEXT_SUMMARIZATION":
        text = params.get("text")
        if not isinstance(text, str):
            raise GeneralError("Invalid text input.")
        # Deterministic local summary: first 3 sentences
        sentences = text.split(".")
        summary = ".".join(sentences[:3]).strip()
        return {"summary": summary}

    if task_type == "BULK_OPERATION":
        tasks = params.get("tasks")
        if not isinstance(tasks, list):
            raise GeneralError("Invalid bulk task list.")
        # Execution is handled elsewhere (dispatcher-level control)
        return {"count": len(tasks)}

    raise GeneralError("Unsupported general task.")
