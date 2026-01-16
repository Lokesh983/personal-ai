"""
STRICT extraction patterns.
Only explicit, literal matches are allowed.
"""

TECHNICAL_SKILL_PATTERNS = [
    r"\bPython\b",
    r"\bSQL\b",
    r"\bREST APIs\b",
]

TOOLS_AND_TECH_PATTERNS = [
    r"\bGit\b",
    r"\bGitHub\b",
    r"\bDocker\b",
    r"\bReact(?:\.js)?\b",
    r"\bNode\.js\b",
    r"\bn8n\b",
]

SOFT_SKILL_PATTERNS = [
    r"\bcommunication skills\b",
    r"\bteamwork\b",
    r"\bleadership\b",
]

DOMAIN_KNOWLEDGE_PATTERNS = [
    r"\bFacial Recognition System\b",
    r"\bidentity verification\b",
    r"\bbehavioral security\b",
]

CERTIFICATION_PATTERNS = [
    r"\bGoogle Introduction to Generative AI\b",
]

ROLE_SPECIFIC_PATTERNS = [
    r"\bfrontend development\b",
    r"\bAPI development\b",
]
