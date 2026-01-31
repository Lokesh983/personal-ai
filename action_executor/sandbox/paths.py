# sandbox/paths.py

import os

from constants.paths import WORKSPACE_ROOT, ALLOWED_PATHS


class PathError(Exception):
    pass


def _contains_forbidden_chars(path: str) -> bool:
    forbidden = ["*", "?", "~", "$", ";", "|", "&"]
    return any(ch in path for ch in forbidden)


def normalize_and_validate_path(input_path: str) -> str:
    """
    Returns a safe, absolute, normalized path inside the workspace.
    Raises PathError on any violation.
    """

    # ---- 1. Type & emptiness ----
    if not isinstance(input_path, str) or not input_path.strip():
        raise PathError("Invalid or unsafe path. Execution aborted.")

    # ---- 2. Forbidden characters ----
    if _contains_forbidden_chars(input_path):
        raise PathError("Invalid or unsafe path. Execution aborted.")

    # ---- 3. Normalize ----
    normalized = os.path.normpath(input_path)

    # ---- 4. Absolute resolution ----
    abs_path = os.path.abspath(normalized)

    # ---- 5. Workspace root enforcement ----
    workspace_root = os.path.abspath(WORKSPACE_ROOT)

    if not abs_path.startswith(workspace_root):
        raise PathError("Invalid or unsafe path. Execution aborted.")

    # ---- 6. Disallow root workspace access ----
    if abs_path == workspace_root:
        raise PathError("Invalid or unsafe path. Execution aborted.")

    # ---- 7. Allowed subdirectories enforcement ----
    allowed = False
    for allowed_root in ALLOWED_PATHS:
        allowed_root_abs = os.path.abspath(allowed_root)
        if abs_path.startswith(allowed_root_abs):
            allowed = True
            break

    if not allowed:
        raise PathError("Invalid or unsafe path. Execution aborted.")

    # ---- 8. Symlink escape protection ----
    real_path = os.path.realpath(abs_path)
    if not real_path.startswith(workspace_root):
        raise PathError("Invalid or unsafe path. Execution aborted.")

    return abs_path
