import time
from urllib.parse import urlencode

from selenium import webdriver


def page_fetcher(url: str, params: dict[str, str | int]) -> str:
    driver = webdriver.Chrome()
    driver.get(f"{url}?{urlencode(params)}")
    time.sleep(20)
    html_source = driver.page_source
    driver.quit()

    return html_source
