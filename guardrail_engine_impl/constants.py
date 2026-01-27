# constants.py

SUPPORTED_TASK_TYPES = {
    # General
    "TEXT_SUMMARIZATION",
    "BULK_OPERATION",

    # Filesystem
    "FILE_READ",
    "FILE_WRITE",
    "FILE_DELETE",
    "FOLDER_CREATE",

    # System
    "SYSTEM_COMMAND",
    "RUN_TOOL",
    "APPLICATION_OPEN",

    # Internet
    "INTERNET_SEARCH",
    "WEB_SCRAPE",
    "API_REQUEST",

    # Download
    "DOWNLOAD_FILE",
}

RULE_CATEGORIES = {
    "OPERATIONS",
    "IO_FILESYSTEM",
    "IO_NETWORK",
    "SYS_COMMANDS",
    "APP_AUTOMATION",
    "CONFIRMATION",
    "INTEGRITY",
    "SAFETY",
}

ALLOWED_REASON_STRINGS = {
    "All checks passed.",
    "One or more rule checks failed.",
}
