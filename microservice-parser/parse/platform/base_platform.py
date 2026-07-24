from abc import ABC, abstractmethod
from datetime import datetime
from xml.etree.ElementTree import Element

from bs4.element import ResultSet, Tag

from core.config import settings


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    def __init__(
        self,
        base_platform: str,
        keyword_id: int,
        page_source: str,
    ) -> None:
        self.base_platform = base_platform
        self.keyword_id = keyword_id
        self.html_source = page_source

    @abstractmethod
    def get_cards_data(self) -> list[Element] | ResultSet[Tag]:
        """Получение блока с тендерами"""

    @abstractmethod
    def is_tender_name_taken(
        self,
        card: Tag | Element,
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
    def get_end_date(card: Tag | Element) -> datetime | None:
        """Метод для определения даты окончания тендера"""

    def search_tenders(
        self, code: str
    ) -> list[dict[str, str | datetime | None | int]]:

        cards = self.get_cards_data()

        tenders = []
        for card in cards:
            title_and_url = self.is_tender_name_taken(card)
            if title_and_url is None:
                continue

            title, url = title_and_url

            if self.base_platform != settings.platforms.sber:
                url = fr"{self.base_platform}{url}"

            tenders.append(
                {
                    "title": f"{title}",
                    "code": code,
                    "pub_date": f"{self.is_tender_pub_date_taken(card)}",
                    "price": f"{self.is_tender_price_taken(card)}",
                    "organizer": f"{self.is_tender_organize_taken(card)}",
                    "url": url,
                    "keyword_id": self.keyword_id,
                    "end_date": f"{self.get_end_date(card)}",
                },
            )

        return tenders
