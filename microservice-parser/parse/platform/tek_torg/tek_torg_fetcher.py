from core.config import settings
import requests

TIMEOUT = 10
HEADERS = settings.header_requests


def page_fetcher(
    url: str,
    params: dict[str, str | int],
) -> str:
    response = requests.get(
        url=url,
        params=params,
        timeout=TIMEOUT,
        headers=HEADERS,
    )
    return response.text
