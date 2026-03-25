import hashlib
import os
import re

from docx import Document
from PyPDF2 import PdfReader

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

_URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
_EMAIL_RE = re.compile(r"@")
_MANY_DIGITS_RE = re.compile(r"(?:\D*\d){7,}")
_PROFILE_RE = re.compile(r"linkedin|github|\.com/", re.IGNORECASE)


def _is_contact_or_noise_line(line: str) -> bool:
    if _EMAIL_RE.search(line):
        return True
    if _URL_RE.search(line):
        return True
    if _MANY_DIGITS_RE.search(line):
        return True
    if _PROFILE_RE.search(line):
        return True
    return False


def _clean_lines_for_preview(text: str) -> list[str]:
    cleaned = []
    for raw_line in text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line:
            continue
        if _is_contact_or_noise_line(line):
            continue
        words = line.split()
        if len(words) < 7:
            continue
        # Skip mostly-uppercase headers and list-like skill fragments.
        alpha_chars = [ch for ch in line if ch.isalpha()]
        if alpha_chars:
            upper_ratio = sum(
                1 for ch in alpha_chars if ch.isupper()) / len(alpha_chars)
            if upper_ratio > 0.8 and len(words) <= 12:
                continue
        if line.count(":") >= 1 and len(words) <= 14:
            continue
        if line.count("|") >= 1:
            continue
        cleaned.append(line)
    return cleaned


def _meaningful_sentences(text: str) -> list[str]:
    raw_parts = [part.strip() for part in text.split(".")]
    sentences = []
    for part in raw_parts:
        if not part:
            continue
        if _is_contact_or_noise_line(part):
            continue
        if len(part.split()) < 7:
            continue
        sentences.append(part)
    return sentences


def _read_file_for_summary(file_path: str):
    if not os.path.exists(file_path):
        return None, "File not found."

    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".pdf":
            reader = PdfReader(file_path)
            extracted_text = ""
            for page in reader.pages:
                extracted_text += page.extract_text() or ""
            extracted_text = _clean_pdf_extraction(extracted_text)
            if not extracted_text:
                return None, "Unable to extract text from file."
            return extracted_text, ""

        if extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file_handle:
                extracted_text = file_handle.read().strip()
            if not extracted_text:
                return None, "Unable to extract text from file."
            return extracted_text, ""

        if extension == ".docx":
            document = Document(file_path)
            extracted_paragraphs = [
                paragraph.text for paragraph in document.paragraphs]
            extracted_text = "\n".join(extracted_paragraphs).strip()
            if not extracted_text:
                return None, "Unable to extract text from file."
            return extracted_text, ""

        with open(file_path, "r", encoding="utf-8") as file_handle:
            extracted_text = file_handle.read().strip()
        if not extracted_text:
            return None, "Unable to extract text from file."
        return extracted_text, ""
    except UnicodeDecodeError:
        return None, "Unable to extract text from file."
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
        file_prefix = re.match(
            r"^(?:the\s+)?file\s+(.+)$", target, re.IGNORECASE)
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


def _clean_pdf_extraction(text: str) -> str:
    """Remove PDF extraction artifacts: soft hyphens, word breaks, excess whitespace."""
    # Remove soft hyphens
    text = text.replace("\u00ad", "")

    # De-hyphenate: join lines broken by hyphens at end of line
    # Pattern: word- \n word → word word
    text = re.sub(r"-\s+([a-z])", r"\1", text, flags=re.IGNORECASE)

    # Normalize multiple spaces/newlines to single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def _normalize_text_for_preview(text: str) -> str:
    normalized = text.replace("\u00ad", "")
    normalized = re.sub(r"\s*-\s*", "-", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def _extract_candidate_lines(text: str) -> list[str]:
    candidates = []
    for raw_line in text.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip(" -\t")
        if not line:
            continue
        if _is_contact_or_noise_line(line):
            continue
        candidates.append(line)
    return candidates


def _is_likely_header(line: str) -> bool:
    words = line.split()
    if not words or len(words) > 7:
        return False
    if line.endswith(":"):
        return True
    if line.isupper() and len(words) <= 5:
        return True
    if all(word[:1].isupper() for word in words if word.isalpha()) and len(words) <= 4:
        return True
    return False


def _build_list_style_summary(lines: list[str]) -> str:
    headers = []
    items = []
    for line in lines:
        if _is_likely_header(line):
            if line not in headers:
                headers.append(line)
            continue
        word_count = len(line.split())
        if 1 <= word_count <= 6 and line not in items:
            items.append(line)

    header_part = ", ".join(headers[:3]) if headers else "multiple sections"
    item_part = ", ".join(items[:6]) if items else "several named entries"

    return (
        "This document is primarily a categorized reference list rather than a continuous narrative. "
        f"It is organized into sections such as {header_part}. "
        f"Representative entries include {item_part}. "
        "Overall, the content is best interpreted as a structured catalogue of organizations, topics, or options for quick lookup."
    )


def _build_narrative_summary(text: str) -> str:
    section_words = re.compile(
        r"\b(PROFESSIONAL\s+SUMMARY|SKILLS|PROJECTS|EDUCATION|TECHNICAL\s+EXPERTISE|ACHIEVEMENTS|LEADERSHIP)\b",
        re.IGNORECASE,
    )

    line_candidates = []
    for line in _extract_candidate_lines(text):
        line = section_words.sub(" ", line)
        if "|" in line:
            parts = [part.strip() for part in line.split("|") if part.strip()]
            if parts:
                line = max(parts, key=lambda value: len(value.split()))
        line = re.sub(r"\s+", " ", line).strip(" -:,")

        if not line:
            continue
        if _is_likely_header(line):
            continue
        if line.count(":") >= 1 and len(line.split()) <= 20:
            continue
        if len(line.split()) < 8:
            continue
        if line not in line_candidates:
            line_candidates.append(line)

    if len(line_candidates) < 3:
        sentence_candidates = []
        for sentence in _meaningful_sentences(text):
            sentence = section_words.sub(" ", sentence)
            sentence = re.sub(r"\s+", " ", sentence).strip(" -:,")
            if len(sentence.split()) < 8:
                continue
            if sentence not in sentence_candidates:
                sentence_candidates.append(sentence)
        if sentence_candidates:
            line_candidates = sentence_candidates

    selected = line_candidates[:5]
    if not selected:
        return ""

    summary_parts = [f"This document highlights {selected[0]}."]
    if len(selected) > 1:
        summary_parts.append(f"It emphasizes {selected[1]}.")
    if len(selected) > 2:
        summary_parts.append(f"It further covers {selected[2]}.")
    if len(selected) > 3:
        summary_parts.append(f"Additionally, {selected[3]}.")
    if len(selected) > 4:
        summary_parts.append(f"It also notes {selected[4]}.")

    return " ".join(summary_parts).strip()


def _summary_preview_from_payload(payload: dict) -> str:
    raw_task = payload.get("raw_input_snapshot", {})
    if raw_task.get("task_type") != "TEXT_SUMMARIZATION":
        return ""
    text = raw_task.get("task_parameters", {}).get("text", "")
    if not isinstance(text, str):
        return ""

    lines = _extract_candidate_lines(text)
    list_like_count = sum(1 for line in lines if len(line.split()) <= 6)
    list_density = (list_like_count / len(lines)) if lines else 0.0

    if len(lines) >= 8 and list_density >= 0.45:
        return _build_list_style_summary(lines)

    normalized_text = _normalize_text_for_preview(text)
    narrative = _build_narrative_summary(normalized_text)
    if narrative:
        return narrative

    cleaned_lines = _clean_lines_for_preview(text)
    if cleaned_lines:
        return " ".join(cleaned_lines[:10]).strip()

    fallback = re.sub(r"\s+", " ", text).strip()
    return fallback[:800].strip()


def run_command(command: str):
    response = {
        "success": False,
        "message": "",
        "summary": "",
        "raw_result": None,
    }

    _prepare_demo_workspace()
    payload, payload_error = _build_executor_payload(command)

    if payload_error:
        print("Attempt 1/3")
        print("❌ Failed")
        print(payload_error)
        response["success"] = False
        response["message"] = payload_error
        response["raw_result"] = None
        return response

    last_result = None
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt}/{MAX_RETRIES}")
        last_result = handle_request(payload, user_confirmation=None)

        if _is_success(last_result):
            message_text = _result_message(last_result) or ""
            summary_preview = _summary_preview_from_payload(payload) or ""

            print("✅ Success")
            if summary_preview:
                print(f"Summary: {summary_preview}")
            else:
                print(_result_message(last_result))

            response["success"] = True
            response["message"] = message_text
            response["summary"] = summary_preview
            response["raw_result"] = last_result
            return response

    print("❌ Failed")
    print(_result_message(last_result))
    response["success"] = False
    response["message"] = _result_message(last_result) or "Execution failed."
    response["summary"] = ""
    response["raw_result"] = last_result
    return response


if __name__ == "__main__":
    while True:
        cmd = input(">> ")
        run_command(cmd)
