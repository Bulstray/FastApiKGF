from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time


def page_fetcher(keyword: str) -> str:

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get('https://www.sberbank-ast.ru/Default.aspx')

    search_box = driver.find_element(
        By.ID,
        "txtUnitedPurchaseSearch",
    )

    time.sleep(10)

    search_box.send_keys(keyword)
    search_box.send_keys(Keys.ENTER)

    time.sleep(10)

    filter_button = driver.find_element(
        By.CSS_SELECTOR,
        "button.element-in-one-row.simple-button.orange-background",
    )
    filter_button.click()

    time.sleep(3)

    stage_event = driver.find_element(
        By.CSS_SELECTOR, 'input.shortdict-filter-choose-button'
    )
    stage_event.click()

    time.sleep(3)

    checkbox = driver.find_element(
        By.XPATH, "//tr[contains(., 'Подача заявок')]//input[@type='checkbox']"
    )
    checkbox.click()

    driver.execute_script("applyModal();")

    driver.execute_script("applyMainFilters();")

    time.sleep(10)

    source_html = driver.page_source

    driver.quit()

    return source_html


