from typing import Dict, List
from collections import OrderedDict

FINAL_KEYS = [
    "technical_skills",
    "soft_skills",
    "tools_and_technologies",
    "domain_knowledge",
    "certifications",
    "role_specific_skills",
    "other_skills",
]


def format_output(normalized: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Formats normalized skills into the final strict JSON schema.
    Ensures deterministic key order and presence of all keys.
    """
    output = OrderedDict()

    for key in FINAL_KEYS:
        value = normalized.get(key, [])
        output[key] = value if isinstance(value, list) else []

    return output
