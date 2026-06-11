import requests

from bs4 import BeautifulSoup
from core.config import settings

TIMEOUT = 10


def get_params(keyword: str):
    return {
        "searchString": keyword,
        "morphology": "on",
        "search-filter": "Дате+размещения",
        "pageNumber": 1,
        "sortDirection": "false",
        "recordsPerPage": "_10",
        "showLotsInfoHidden": "false",
        "sortBy": "UPDATE_DATE",
        "fz44": "on",
        "fz223": "on",
        "af": "on",
        "currencyIdGeneral": "-1",
    }


def page_fetcher(
    keyword: str,
) -> str:
    response = requests.get(
        url=settings.platforms.zakupki_gov_search,
        timeout=TIMEOUT,
        params=get_params(keyword),
        headers=settings.header_requests,
    )

    return response.text
