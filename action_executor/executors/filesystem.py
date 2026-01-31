# executors/filesystem.py

import os

from sandbox.paths import normalize_and_validate_path, PathError
from constants.limits import MAX_FILE_SIZE_MB


class FilesystemError(Exception):
    pass


def filesystem_executor(task: dict) -> dict:
    """
    Executes exactly one filesystem action.
    """

    task_type = task.get("task_type")
    params = task.get("task_parameters")

    if not isinstance(params, dict):
        raise FilesystemError("Invalid task parameters.")

    try:
        # -------- FILE_READ --------
        if task_type == "FILE_READ":
            path = normalize_and_validate_path(params.get("path"))
            if not os.path.isfile(path):
                raise FilesystemError("File does not exist.")

            with open(path, "r", encoding="utf-8") as f:
                return {"content": f.read()}

        # -------- FILE_WRITE --------
        if task_type == "FILE_WRITE":
            path = normalize_and_validate_path(params.get("path"))
            content = params.get("content")

            if not isinstance(content, str):
                raise FilesystemError("Invalid file content.")

            parent_dir = os.path.dirname(path)
            if not os.path.isdir(parent_dir):
                raise FilesystemError("Parent directory does not exist.")

            size_mb = len(content.encode("utf-8")) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                raise FilesystemError("File size exceeds limit.")

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            return {"status": "written"}

        # -------- FILE_DELETE --------
        if task_type == "FILE_DELETE":
            path = normalize_and_validate_path(params.get("path"))
            if not os.path.isfile(path):
                raise FilesystemError("File does not exist.")

            os.remove(path)
            return {"status": "deleted"}

        # -------- FOLDER_CREATE --------
        if task_type == "FOLDER_CREATE":
            path = normalize_and_validate_path(params.get("path"))

            parent_dir = os.path.dirname(path)
            if not os.path.isdir(parent_dir):
                raise FilesystemError("Parent directory does not exist.")

            if os.path.exists(path):
                raise FilesystemError("Folder already exists.")

            os.mkdir(path)
            return {"status": "created"}

        raise FilesystemError("Unsupported filesystem task type.")

    except (PathError, OSError) as e:
        raise FilesystemError(str(e))
