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
    },
    "CLOSE_CHROME": {
        "binary": "C:\\Windows\\System32\\taskkill.exe",
        "allowed_args": ["/IM", "chrome.exe", "/F"],
        "expected_exit_code": 0
    },
    "CLOSE_BRAVE": {
        "binary": "C:\\Windows\\System32\\taskkill.exe",
        "allowed_args": ["/IM", "brave.exe", "/F"],
        "expected_exit_code": 0
    },
    "CLOSE_EDGE": {
        "binary": "C:\\Windows\\System32\\taskkill.exe",
        "allowed_args": ["/IM", "msedge.exe", "/F"],
        "expected_exit_code": 0
    },
    "CLOSE_TELEGRAM": {
        "binary": "C:\\Windows\\System32\\taskkill.exe",
        "allowed_args": ["/IM", "Telegram.exe", "/F"],
        "expected_exit_code": 0
    },
    "CLOSE_WHATSAPP": {
        "binary": "C:\\Windows\\System32\\taskkill.exe",
        "allowed_args": ["/IM", "WhatsApp.Root.exe", "/F"],
        "expected_exit_code": 0
    }
}
