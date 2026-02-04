from abc import ABC, abstractmethod

from bs4.element import Tag

from core.models import Tender

import requests

from core.enums import Platform


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    TIMEOUT = 10

    def __init__(
        self,
        base_url: str,
        params: dict,
    ) -> None:
        self.base_url = base_url
        self.response = requests.get(
            url=self.base_url,
            params=params,
            timeout=self.TIMEOUT,
        )

    @staticmethod
    @abstractmethod
    def get_params(key_word: str) -> dict:
        """Возвращает параметры запроса"""

    @abstractmethod
    def get_cards_data(self) -> dict[str, str | int | list[str]]:
        """Получение блока с тендерами"""

    @staticmethod
    @abstractmethod
    def is_tender_name_taken(card: Tag) -> str:
        """Метод для проверки имени тендера"""

    @staticmethod
    @abstractmethod
    def is_tender_pub_date_taken(card: Tag) -> str:
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
