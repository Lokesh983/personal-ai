from core.confirmation import confirmation_required
from executors.filesystem import filesystem_executor
from executors.system import system_executor
from executors.internet import internet_executor
from executors.download import download_executor
from executors.general import general_executor


class DispatchError(Exception):
    pass


_DISPATCH_TABLE = {
    "FILE_READ": filesystem_executor,
    "FILE_WRITE": filesystem_executor,
    "FILE_DELETE": filesystem_executor,
    "FOLDER_CREATE": filesystem_executor,

    "SYSTEM_COMMAND": system_executor,
    "APPLICATION_OPEN": system_executor,

    "INTERNET_SEARCH": internet_executor,
    "WEB_SCRAPE": internet_executor,
    "API_REQUEST": internet_executor,

    "DOWNLOAD_FILE": download_executor,

    "TEXT_SUMMARIZATION": general_executor,
    "BULK_OPERATION": general_executor,
}


def dispatch(task: dict, guardrail_decision: dict):
    """
    Returns one of:
    - ('PAUSE', None)
    - ('EXECUTE', executor_function)
    Raises DispatchError on violation
    """

    task_type = task.get("task_type")

    if task_type not in _DISPATCH_TABLE:
        raise DispatchError("Task dispatch violation. Execution aborted.")

    # ---- Confirmation gate ----
    if confirmation_required(task_type, guardrail_decision):
        return "PAUSE", None

    executor = _DISPATCH_TABLE[task_type]
    return "EXECUTE", executor
