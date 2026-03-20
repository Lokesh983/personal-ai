import hashlib
import os
import re

from docx import Document
from pypdf import PdfReader

from action_executor.main import handle_request


MAX_RETRIES = 3
DEMO_TIMESTAMP = "2026-03-20T00:00:00Z"
DEMO_SOURCE_ID = "runner-demo"
DEMO_SCHEMA_VERSION = "1.0.0"
DEMO_WORKSPACE_ROOT = "C:/Users/Lokesh/Desktop/test"

APP_CLOSE_COMMANDS = {
    "chrome": ("CLOSE_CHROME", ["/IM", "chrome.exe", "/F"]),
    "brave": ("CLOSE_BRAVE", ["/IM", "brave.exe", "/F"]),
    "edge": ("CLOSE_EDGE", ["/IM", "msedge.exe", "/F"]),
    "telegram": ("CLOSE_TELEGRAM", ["/IM", "Telegram.exe", "/F"]),
    "whatsapp": ("CLOSE_WHATSAPP", ["/IM", "WhatsApp.Root.exe", "/F"]),
}


def _read_file_for_summary(file_path: str):
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".pdf":
            reader = PdfReader(file_path)
            extracted_pages = [
                page.extract_text() or "" for page in reader.pages]
            extracted_text = "\n".join(extracted_pages).strip()
            if not extracted_text:
                return None, "Unable to extract text from PDF file."
            return extracted_text, ""

        if extension == ".docx":
            document = Document(file_path)
            extracted_paragraphs = [
                paragraph.text for paragraph in document.paragraphs]
            extracted_text = "\n".join(extracted_paragraphs).strip()
            if not extracted_text:
                return None, "Unable to extract text from DOCX file."
            return extracted_text, ""

        with open(file_path, "r", encoding="utf-8") as file_handle:
            return file_handle.read(), ""
    except UnicodeDecodeError:
        return None, "Unable to summarize this file type. Use UTF-8 text, PDF, or DOCX."
    except OSError as exc:
        return None, f"Unable to read file for summarization: {exc}"
    except Exception as exc:
        return None, f"Unable to parse file for summarization: {exc}"


def _build_base_payload(command: str) -> dict:
    # Keep the requested demo payload shape available as the runner input envelope.
    return {
        "raw_input": command,
        "raw_input_snapshot": {"text": command},
        "guardrail_decision": {},
        "external_timestamp": ""
    }


def _stable_task_id(command: str) -> str:
    digest = hashlib.sha1(command.encode("utf-8")).hexdigest()[:10]
    return f"task-{digest}"


def _normalize_demo_path(path_value: str) -> str:
    candidate = path_value.strip().strip('"').strip("'")
    if not candidate:
        return ""
    if "/" in candidate or "\\" in candidate or os.path.isabs(candidate):
        return candidate
    return f"{DEMO_WORKSPACE_ROOT}/{candidate}"


def _command_to_task(command: str):
    text = command.strip()
    lowered = text.lower()

    if lowered.startswith("open "):
        app_name = text[5:].strip().strip('"').strip("'")
        return {
            "task_type": "APPLICATION_OPEN",
            "task_parameters": {"app_name": app_name},
        }, ""

    if lowered.startswith("close "):
        app_name = text[6:].strip().strip('"').strip("'").lower()
        if app_name not in APP_CLOSE_COMMANDS:
            supported_apps = ", ".join(sorted(APP_CLOSE_COMMANDS.keys()))
            return None, f"Unsupported app for close command. Supported apps: {supported_apps}"
        command_id, args = APP_CLOSE_COMMANDS[app_name]
        return {
            "task_type": "SYSTEM_COMMAND",
            "task_parameters": {
                "command_id": command_id,
                "args": args,
            },
        }, ""

    create_match = re.match(
        r"^create\s+file\s+(.+?)\s+with\s+content\s+(.+)$", text, re.IGNORECASE)
    if create_match:
        file_name = _normalize_demo_path(create_match.group(1))
        content = create_match.group(2).strip().strip('"').strip("'")
        if not file_name:
            return None, "Invalid file path."
        return {
            "task_type": "FILE_WRITE",
            "task_parameters": {
                "path": file_name,
                "content": content,
            },
        }, ""

    if lowered.startswith("summarize "):
        target = text[len("summarize "):].strip()
        file_prefix = re.match(r"^file\s+(.+)$", target, re.IGNORECASE)
        if file_prefix:
            file_path = _normalize_demo_path(file_prefix.group(1))
            extracted_text, extraction_error = _read_file_for_summary(
                file_path)
            if extraction_error:
                return None, extraction_error
            target = extracted_text
        return {
            "task_type": "TEXT_SUMMARIZATION",
            "task_parameters": {"text": target},
        }, ""

    return None, "Unsupported command. Use: open <app>, close <app>, create file <name> with content <text>, summarize <text or file>."


def _prepare_demo_workspace() -> None:
    os.makedirs(DEMO_WORKSPACE_ROOT, exist_ok=True)


def _build_executor_payload(command: str):
    _ = _build_base_payload(command)
    task, parse_error = _command_to_task(command)
    if parse_error:
        return None, parse_error

    raw_task = {
        "task_id": _stable_task_id(command),
        "task_type": task["task_type"],
        "task_parameters": task["task_parameters"],
        "task_source_id": DEMO_SOURCE_ID,
        "task_schema_version": DEMO_SCHEMA_VERSION,
    }

    return {
        "raw_input_snapshot": raw_task,
        "guardrail_decision": {
            "approved": True,
            "required_confirmation": False,
        },
        "external_timestamp": DEMO_TIMESTAMP,
    }, ""


def _is_success(result) -> bool:
    if isinstance(result, dict):
        if result.get("executed") is True:
            return True
        result_text = str(result).lower()
        return "success" in result_text and "failed" not in result_text
    return False


def _result_message(result) -> str:
    if isinstance(result, dict):
        if result.get("details"):
            return str(result["details"])
        if result.get("error"):
            return str(result["error"])
        log_entry = result.get("log_entry", {})
        if isinstance(log_entry, dict) and log_entry.get("executor_result"):
            return str(log_entry["executor_result"])
    return str(result)


def _summary_preview_from_payload(payload: dict) -> str:
    raw_task = payload.get("raw_input_snapshot", {})
    if raw_task.get("task_type") != "TEXT_SUMMARIZATION":
        return ""
    text = raw_task.get("task_parameters", {}).get("text", "")
    if not isinstance(text, str):
        return ""
    sentences = text.split(".")
    return ".".join(sentences[:3]).strip()


def run_command(command: str):
    _prepare_demo_workspace()
    payload, payload_error = _build_executor_payload(command)

    if payload_error:
        print("Attempt 1/3")
        print("❌ Failed")
        print(payload_error)
        return {"executed": False, "error": payload_error}

    last_result = None
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt}/{MAX_RETRIES}")
        last_result = handle_request(payload, user_confirmation=None)

        if _is_success(last_result):
            print("✅ Success")
            summary_preview = _summary_preview_from_payload(payload)
            if summary_preview:
                print(f"Summary: {summary_preview}")
            else:
                print(_result_message(last_result))
            return last_result

    print("❌ Failed")
    print(_result_message(last_result))
    return last_result


if __name__ == "__main__":
    while True:
        cmd = input(">> ")
        run_command(cmd)
