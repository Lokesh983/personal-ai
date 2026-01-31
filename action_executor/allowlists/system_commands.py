SAFE_SYSTEM_COMMANDS = {
    "LIST_DIRECTORY": {
        "binary": "/bin/ls",
        "allowed_args": ["-l"],
        "expected_exit_code": 0
    },
    "CHECK_DISK_USAGE": {
        "binary": "/bin/df",
        "allowed_args": ["-h"],
        "expected_exit_code": 0
    }
}
