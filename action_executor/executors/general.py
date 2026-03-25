import re


class GeneralError(Exception):
    pass


_URL_RE = re.compile(r"https?://|www\.", re.IGNORECASE)
_EMAIL_RE = re.compile(r"@")
_MANY_DIGITS_RE = re.compile(r"(?:\D*\d){7,}")


def _split_sentences(text: str) -> list[str]:
    parts = [part.strip() for part in text.split(".")]
    return [part for part in parts if part]


def _is_contact_or_noise_line(line: str) -> bool:
    if _EMAIL_RE.search(line):
        return True
    if _URL_RE.search(line):
        return True
    if _MANY_DIGITS_RE.search(line):
        return True
    return False


def _clean_text_for_summary(text: str) -> str:
    cleaned_lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if _is_contact_or_noise_line(line):
            continue
        if len(line.split()) < 5:
            continue
        cleaned_lines.append(line)
    return " ".join(cleaned_lines).strip()


def _first_three_sentences(text: str) -> str:
    sentences = _split_sentences(text)
    return ". ".join(sentences[:3]).strip()


def _first_three_meaningful_sentences(text: str) -> str:
    selected = []
    for sentence in _split_sentences(text):
        if len(sentence.split()) < 5:
            continue
        if _is_contact_or_noise_line(sentence):
            continue
        selected.append(sentence)
        if len(selected) == 3:
            break
    return ". ".join(selected).strip()


def general_executor(task: dict) -> dict:
    task_type = task["task_type"]
    params = task["task_parameters"]

    if task_type == "TEXT_SUMMARIZATION":
        text = params.get("text")
        if not isinstance(text, str):
            raise GeneralError("Invalid text input.")

        cleaned_text = _clean_text_for_summary(text)

        # Fallback safety: if cleaned text is too short, use raw text strategy.
        if len(_split_sentences(cleaned_text)) < 2 or len(cleaned_text.split()) < 12:
            summary = _first_three_sentences(text)
        else:
            summary = _first_three_meaningful_sentences(cleaned_text)
            if not summary:
                summary = _first_three_sentences(text)

        return {"summary": summary}

    if task_type == "BULK_OPERATION":
        tasks = params.get("tasks")
        if not isinstance(tasks, list):
            raise GeneralError("Invalid bulk task list.")
        # Execution is handled elsewhere (dispatcher-level control)
        return {"count": len(tasks)}

    raise GeneralError("Unsupported general task.")
