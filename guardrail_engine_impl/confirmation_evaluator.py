# confirmation_evaluator.py

class ConfirmationEvaluator:
    def evaluate(self, task: dict) -> bool:
        task_type = task.get("task_type")
        params = task.get("task_parameters", {})

        # Destructive or bulk filesystem actions
        if task_type in {
            "FILE_DELETE",
            "BULK_OPERATION",
        }:
            return True

        # Internet-related actions
        if task_type in {
            "WEB_SCRAPE",
            "API_REQUEST",
            "DOWNLOAD_FILE",
        }:
            return True

        # System-level actions
        if task_type in {
            "SYSTEM_COMMAND",
            "RUN_TOOL",
            "APPLICATION_OPEN",
        }:
            return True

        return False
