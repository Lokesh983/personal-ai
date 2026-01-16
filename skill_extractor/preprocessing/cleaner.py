# skill_extractor/preprocessing/cleaner.py

import re


def clean_text(raw_text: str) -> str:
    """
    Cleans raw text by normalizing whitespace and blank lines
    without altering content meaning or casing.
    """
    if not raw_text:
        return ""

    # Normalize line endings
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")

    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.split("\n")]

    # Remove consecutive blank lines
    cleaned_lines = []
    prev_blank = False

    for line in lines:
        if line == "":
            if not prev_blank:
                cleaned_lines.append(line)
            prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False

    return "\n".join(cleaned_lines)
