# skill_extractor/preprocessing/splitter.py

import re

BULLET_PATTERN = re.compile(r"^\s*[-•*]\s+")


def split_text(clean_text: str) -> list[str]:
    """
    Splits cleaned text into sentence-like units using
    structural delimiters only.
    """
    if not clean_text:
        return []

    segments = []

    for line in clean_text.split("\n"):
        if not line:
            continue

        # Handle bullet points
        if BULLET_PATTERN.match(line):
            segments.append(BULLET_PATTERN.sub("", line))
            continue

        # Split on period followed by space + capital letter
        parts = re.split(r"(?<=\.)\s+(?=[A-Z])", line)
        for part in parts:
            part = part.strip()
            if part:
                segments.append(part)

    return segments
