from abc import ABC, abstractmethod
from xml.etree.ElementTree import Element

import requests
from bs4.element import ResultSet, Tag

from core.enums import Platform
from core.models import Tender


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    TIMEOUT = 10

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

    def search_tenders(self, platform: Platform) -> list[Tender]:

        cards = self.get_cards_data()

        return [
            Tender(
                platform=platform,
                name=self.is_tender_name_taken(card=card),
                pub_date=self.is_tender_pub_date_taken(card=card),
            )
            for card in cards
        ]
