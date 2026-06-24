import time
from urllib.parse import urlencode
from core.config import settings

from selenium import webdriver


def get_params(key_word: str) -> dict[str, str | int]:
    return {
        "page": 1,
        "per": 100,
        "procedure[stage][0]": "accepting",
        "search": key_word,
        "sort": "by_relevance",
    }


def page_fetcher(key_word: str) -> str:
    driver = webdriver.Chrome()
    driver.get(
        f"{settings.platforms.etp_gpb}?{urlencode(get_params(key_word))}"
    )
    time.sleep(15)
    html_source = driver.page_source
    driver.quit()

    return html_source
