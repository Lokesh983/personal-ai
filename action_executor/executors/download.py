import requests

from sandbox.paths import normalize_and_validate_path
from constants.limits import MAX_FILE_SIZE_MB
from core.allowlist_enforcer import enforce_network_policy


class DownloadError(Exception):
    pass


def download_executor(task: dict) -> dict:
    params = task["task_parameters"]
    url = params.get("url")
    dest = normalize_and_validate_path(params.get("destination_path"))

    try:
        enforce_network_policy(url)
        r = requests.get(url, stream=True, timeout=5)
        size = 0

        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    size += len(chunk)
                    if size > MAX_FILE_SIZE_MB * 1024 * 1024:
                        raise DownloadError("Downloaded file too large.")
                    f.write(chunk)

        return {"status": "downloaded"}

    except Exception as e:
        raise DownloadError(str(e))
