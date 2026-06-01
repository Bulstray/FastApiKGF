import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def page_fetcher(keyword: str) -> str:
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(
        "https://lukoil.ru/Company/Tendersandauctions/Tenders/TendersofLukoilgroup"
    )

    search_box = driver.find_element(
        By.CSS_SELECTOR, ".form-control.search-control"
    )
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)

    time.sleep(10)

    source_html = driver.page_source

    driver.quit()

    return source_html
