import re
from urllib.parse import urlparse

from allowlists.system_commands import SAFE_SYSTEM_COMMANDS
from allowlists.applications import ALLOWED_APPLICATIONS
from allowlists.network import (
    ALLOWED_PROTOCOLS,
    BLOCKED_PORTS,
    MAX_REQUEST_TIMEOUT_MS
)
from constants.paths import WORKSPACE_ROOT


class AllowlistError(Exception):
    pass


_SHELL_META = re.compile(r"[;&|$`()<>]")


def enforce_system_command(command_id: str, args: list) -> dict:
    if command_id not in SAFE_SYSTEM_COMMANDS:
        raise AllowlistError("SYSTEM_COMMAND not allowlisted.")

    meta = SAFE_SYSTEM_COMMANDS[command_id]

    if not isinstance(args, list):
        raise AllowlistError("Invalid arguments for SYSTEM_COMMAND.")

    for arg in args:
        if arg not in meta["allowed_args"]:
            raise AllowlistError("SYSTEM_COMMAND argument not allowlisted.")
        if _SHELL_META.search(arg):
            raise AllowlistError(
                "SYSTEM_COMMAND argument contains forbidden characters.")

    return {
        "binary": meta["binary"],
        "args": args,
        "expected_exit_code": meta["expected_exit_code"]
    }


def enforce_application_open(app_name: str, platform: str) -> dict:
    if app_name not in ALLOWED_APPLICATIONS:
        raise AllowlistError("Application not allowlisted.")

    app = ALLOWED_APPLICATIONS[app_name]

    if app["platform"] != platform:
        raise AllowlistError("Application not allowed on this platform.")

    return {
        "launch_method": app["launch_method"]
    }


def enforce_network_policy(url: str) -> None:
    parsed = urlparse(url)

    if parsed.scheme not in ALLOWED_PROTOCOLS:
        raise AllowlistError("Network policy violation.")

    if parsed.port and parsed.port in BLOCKED_PORTS:
        raise AllowlistError("Network policy violation.")

    if _SHELL_META.search(url):
        raise AllowlistError("Network policy violation.")

    # Timeout is enforced by the caller using MAX_REQUEST_TIMEOUT_MS
    return None


def enforce_run_tool() -> None:
    raise AllowlistError("RUN_TOOL is disabled in v1.")
