import requests

from core.config import settings

TIMEOUT = 10
HEADERS = settings.header_requests


def get_params(key_word: str) -> dict[str, str | int]:
    return {
        "name": key_word,
        "status[]": "Приём заявок",
    }


def page_fetcher(
    key_word: str,
) -> str:
    response = requests.get(
        url=settings.platforms.tek_torg,
        params=get_params(key_word),
        timeout=TIMEOUT,
        headers=HEADERS,
    )
    return response.text
