import subprocess

from core.allowlist_enforcer import enforce_system_command, enforce_application_open
from constants.platform import EXECUTION_PLATFORM


class SystemError(Exception):
    pass


def system_executor(task: dict) -> dict:
    task_type = task["task_type"]
    params = task["task_parameters"]

    try:
        if task_type == "SYSTEM_COMMAND":
            meta = enforce_system_command(
                params.get("command_id"),
                params.get("args", [])
            )
            result = subprocess.run(
                [meta["binary"], *meta["args"]],
                capture_output=True,
                text=True
            )
            if result.returncode != meta["expected_exit_code"]:
                raise SystemError("SYSTEM_COMMAND execution failed.")
            return {"exit_code": result.returncode}

        if task_type == "APPLICATION_OPEN":
            meta = enforce_application_open(
                params.get("app_name"),
                EXECUTION_PLATFORM
            )
            subprocess.Popen([meta["launch_method"]])
            return {"status": "launched"}

        raise SystemError("Unsupported system task.")

    except Exception as e:
        raise SystemError(str(e))
