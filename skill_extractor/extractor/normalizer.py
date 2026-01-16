from typing import Dict, List

NORMALIZATION_MAP = {
    "Python3": "Python",
    "python 3": "Python",
    "React.js": "React",
}


def normalize_and_deduplicate(
    extracted: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """
    Normalizes skills using a strict whitelist and removes duplicates.
    Applies deterministic alphabetical ordering.
    """
    normalized_output = {}

    for category, skills in extracted.items():
        seen = set()
        cleaned = []

        for skill in skills:
            canonical = NORMALIZATION_MAP.get(skill, skill)

            if canonical not in seen:
                seen.add(canonical)
                cleaned.append(canonical)

        # Deterministic ordering
        cleaned.sort()
        normalized_output[category] = cleaned

    # Global not_found fallback
    all_skills = sum(normalized_output.values(), [])
    if not all_skills:
        normalized_output["other_skills"] = ["not_found"]

    return normalized_output
