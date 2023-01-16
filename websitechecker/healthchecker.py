import re
from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class Health:
    """
    Convenience container for healthcheck data
    """
    timestamp: int  # timestamp in ms
    status_code: int
    time_elapsed: int  # ms
    pattern_found: bool | None


def healthcheck(url: str, match: str | None = None) -> Health:
    """_summary_

    Args:
        url (str): url to query
        match (str | None, optional): Pattern to search in the webpage. Defaults to None.

    Returns:
        Health: Collection of results
    """

    timestamp = int(round(datetime.utcnow().timestamp() * 1000))
    response = requests.get(url=url)

    pattern_found = None
    if match:
        pattern = re.compile(match)
        pattern_found = pattern.search(response.text) is not None

    time_elapsed_ms = response.elapsed.microseconds // 1000

    return Health(
        timestamp=timestamp,
        status_code=response.status_code,
        time_elapsed=time_elapsed_ms,
        pattern_found=pattern_found,
    )
