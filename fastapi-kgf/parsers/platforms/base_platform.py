import time
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from xml.etree.ElementTree import Element

import requests
from bs4.element import ResultSet, Tag
from selenium import webdriver

from core.config import settings
from core.schemas import TenderCreate


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    TIMEOUT = 10
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

    def __init__(
        self,
        base_platform: str,
        base_url: str,
        params: dict[str, str | int],
        keyword_id: int,
    ) -> None:
        self.base_url = base_url
        self.base_platform = base_platform
        self.keyword_id = keyword_id
        if base_url == settings.tender_platform.etp_gpb:
            driver = webdriver.Chrome()
            driver.get(f"{base_url}?{urlencode(params)}")
            time.sleep(20)
            self.html_source = driver.page_source
            driver.quit()
        else:
            self.html_source = requests.get(
                url=self.base_url,
                params=params,
                timeout=self.TIMEOUT,
                headers=self.HEADERS,
            )
            self.html_source = self.html_source.text

    @staticmethod
    @abstractmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        """Возвращает параметры запроса"""

    @abstractmethod
    def get_cards_data(self) -> list[Element] | ResultSet[Tag]:
        """Получение блока с тендерами"""

    @abstractmethod
    def is_tender_name_taken(
        self, card: Tag | Element,
    ) -> tuple[str, str] | None:
        """Метод для проверки имени тендера"""

    @staticmethod
    @abstractmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:
        """Метод для проверки и преобразовании даты публикации"""

    @staticmethod
    @abstractmethod
    def is_tender_price_taken(card: Tag | Element) -> str:
        """Метод для получения цены"""

    @staticmethod
    @abstractmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        """Метод для определения организатора"""

    @staticmethod
    @abstractmethod
    def get_end_date(card: Tag | Element) -> str:
        """Метод для определения даты окончания тендера"""

    def search_tenders(self) -> list[TenderCreate]:

        cards = self.get_cards_data()

        tenders = []
        for card in cards:
            title_and_url = self.is_tender_name_taken(card)
            if title_and_url is None:
                continue

            title, url = title_and_url

            tenders.append(
                TenderCreate(
                    name=title,
                    pub_date=self.is_tender_pub_date_taken(card),
                    price=self.is_tender_price_taken(card),
                    organizer=self.is_tender_organize_taken(card),
                    url=fr"{self.base_platform}{url}",
                    keyword_id=self.keyword_id,
                    end_date=self.get_end_date(card),
                ),
            )

        return tenders
