# logging/audit_log.py

import json
import os

from constants.paths import ALLOWED_PATHS


class LoggingError(Exception):
    pass


# Enforce logs directory from allowed paths
_LOGS_DIR = None
for p in ALLOWED_PATHS:
    if p.endswith("/logs/"):
        _LOGS_DIR = p
        break

if _LOGS_DIR is None:
    raise LoggingError("Logs directory not configured.")


def _ensure_logs_dir():
    if not os.path.isdir(_LOGS_DIR):
        raise LoggingError("Logs directory does not exist.")


def append_log_entry(log_entry: dict) -> None:
    """
    Appends exactly one JSON log entry.
    Raises LoggingError on any failure.
    """
    if not isinstance(log_entry, dict):
        raise LoggingError("Invalid log entry.")

    required_fields = {
        "raw_input_snapshot",
        "guardrail_decision",
        "executor_result",
        "external_timestamp",
    }

    if set(log_entry.keys()) != required_fields:
        raise LoggingError("Invalid log entry schema.")

    _ensure_logs_dir()

    log_file_path = os.path.join(_LOGS_DIR, "executor_audit.log")

    try:
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False))
            f.write("\n")
    except OSError as e:
        raise LoggingError(str(e))
