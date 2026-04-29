from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

import requests
from bs4.element import ResultSet, Tag

from core.schemas import Tender


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    TIMEOUT = 10
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    def __init__(
        self,
        base_url: str,
        params: dict[str, str | int],
    ) -> None:
        self.base_url = base_url
        self.response = requests.get(
            url=self.base_url,
            params=params,
            timeout=self.TIMEOUT,
            headers=self.HEADERS,
        )

    @staticmethod
    @abstractmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        """Возвращает параметры запроса"""

    @abstractmethod
    def get_cards_data(self) -> list[Element] | ResultSet[Tag]:
        """Получение блока с тендерами"""

    @staticmethod
    @abstractmethod
    def is_tender_name_taken(card: Tag | Element) -> str:
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

    def search_tenders(self) -> list[Tender]:

        cards = self.get_cards_data()

        return [
            Tender(
                name=self.is_tender_name_taken(card=card),
                pub_date=self.is_tender_pub_date_taken(card=card),
                price=self.is_tender_price_taken(card=card),
                organizer=self.is_tender_organize_taken(card=card),
            )
            for card in cards
        ]
