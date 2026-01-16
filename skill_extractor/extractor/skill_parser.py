import re
from typing import Dict, List
from extractor import patterns


def extract_skills_from_chunks(chunks: List[str]) -> Dict[str, List[str]]:
    """
    Extracts skills from text chunks using strict regex matching.
    """
    result = {
        "technical_skills": [],
        "soft_skills": [],
        "tools_and_technologies": [],
        "domain_knowledge": [],
        "certifications": [],
        "role_specific_skills": [],
        "other_skills": []
    }

    def _extract(pattern_list, text):
        matches = []
        for pattern in pattern_list:
            found = re.findall(pattern, text)
            matches.extend(found)
        return matches

    for chunk in chunks:
        result["technical_skills"].extend(
            _extract(patterns.TECHNICAL_SKILL_PATTERNS, chunk)
        )
        result["tools_and_technologies"].extend(
            _extract(patterns.TOOLS_AND_TECH_PATTERNS, chunk)
        )
        result["soft_skills"].extend(
            _extract(patterns.SOFT_SKILL_PATTERNS, chunk)
        )
        result["domain_knowledge"].extend(
            _extract(patterns.DOMAIN_KNOWLEDGE_PATTERNS, chunk)
        )
        result["certifications"].extend(
            _extract(patterns.CERTIFICATION_PATTERNS, chunk)
        )
        result["role_specific_skills"].extend(
            _extract(patterns.ROLE_SPECIFIC_PATTERNS, chunk)
        )

    return result
