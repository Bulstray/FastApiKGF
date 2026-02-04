from datetime import datetime

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from core.config import settings
from core.enums import Platform
from core.models import Tender
from parsers.platforms.base_platform import BaseTenderPlatform


class TekTorgPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(self, key_word: str) -> None:
        super().__init__(
            base_url=f"{settings.tender_platform.tek_torg}",
            params=self.get_params(key_word=key_word),
        )

    @staticmethod
    def is_tender_name_taken(card: Tag) -> str:
        name_tag = card.find("a")

        if name_tag is None:
            return "Имя не найдено"

        return name_tag.text

    @staticmethod
    def is_tender_pub_date_taken(card: Tag) -> str:
        pub_date_tag = card.find(
            "span",
            class_="sc-7909e12c-0 glSvLE",
        )
        if pub_date_tag is None:
            return "Дата не найдена"

        pub_date = datetime.strptime(
            pub_date_tag.text,
            "%d.%m.%Y",
        )

        return pub_date.strftime("%Y-%m-%d")

    @staticmethod
    def get_params(key_word: str) -> dict[str, str | list[str]]:
        return {
            "status[]": ["Приём заявок"],
            "name": key_word,
        }

    def get_cards_data(self):
        soup = BeautifulSoup(self.response.text, "html.parser")
        return soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc")
