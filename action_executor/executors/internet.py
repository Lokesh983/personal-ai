import requests

from core.allowlist_enforcer import enforce_network_policy
from constants.limits import MAX_RESPONSE_SIZE_KB


class InternetError(Exception):
    pass


def internet_executor(task: dict) -> dict:
    task_type = task["task_type"]
    params = task["task_parameters"]

    try:
        url = params.get("url")
        enforce_network_policy(url)

        if task_type == "INTERNET_SEARCH":
            r = requests.get(url, timeout=5)
            if len(r.content) > MAX_RESPONSE_SIZE_KB * 1024:
                raise InternetError("Response size exceeded.")
            return {"response": r.text}

        if task_type == "WEB_SCRAPE":
            r = requests.get(url, timeout=5)
            if len(r.content) > MAX_RESPONSE_SIZE_KB * 1024:
                raise InternetError("Response size exceeded.")
            return {"content": r.text}

        if task_type == "API_REQUEST":
            method = params.get("method", "GET")
            payload = params.get("payload")
            if method == "GET":
                r = requests.get(url, timeout=5)
            elif method == "POST":
                r = requests.post(url, json=payload, timeout=5)
            else:
                raise InternetError("Unsupported HTTP method.")
            if len(r.content) > MAX_RESPONSE_SIZE_KB * 1024:
                raise InternetError("Response size exceeded.")
            return {"json": r.json()}

        raise InternetError("Unsupported internet task.")

    except Exception as e:
        raise InternetError(str(e))
