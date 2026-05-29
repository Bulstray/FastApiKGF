from abc import ABC, abstractmethod
from datetime import datetime
from xml.etree.ElementTree import Element

from core.config import settings

from bs4.element import ResultSet, Tag


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

    def search_tenders(self) -> list[dict[str, str | datetime | None | int]]:

        cards = self.get_cards_data()

        tenders = []
        urls = []
        for card in cards:
            title_and_url = self.is_tender_name_taken(card)
            if title_and_url is None:
                continue

            title, url = title_and_url

            if url in urls:
                continue

            urls.append(url)

            tenders.append(
                {
                    "name": f"{title}",
                    "pub_date": f"{self.is_tender_pub_date_taken(card)}",
                    "price": f"{self.is_tender_price_taken(card)}",
                    "organizer": f"{self.is_tender_organize_taken(card)}",
                    "url": (
                        url
                        if self.base_platform == settings.platforms.sber
                        else fr"{self.base_platform}{url}"
                    ),
                    "keyword_id": self.keyword_id,
                    "end_date": f"{self.get_end_date(card)}",
                },
            )

        return tenders
