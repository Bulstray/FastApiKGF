from xml.etree.ElementTree import Element

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from core.config import settings
from parsers.platforms.base_platform import BaseTenderPlatform
from datetime import date

import dateparser


class TekTorgPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(self, key_word: str, keyword_id: int) -> None:
        super().__init__(
            base_url=f"{settings.tender_platform.tek_torg}",
            base_platform=f"{settings.tender_platform.base_platform.base_tek_torg}",
            params=self.get_params(key_word=key_word),
            keyword_id=keyword_id,
        )

    def is_tender_name_taken(
        self, card: Tag | Element
    ) -> tuple[str, str] | None:

        if isinstance(card, Element):
            return None

        name_tag = card.find("a", class_="sc-6c01eeae-7 gccepd")

        if name_tag is None:
            return None

        return f"{name_tag.text}", f"{name_tag.get('href')}"

    @staticmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:

        if isinstance(card, Element):
            return "Дата не найдена"

        pub_date_tag = card.find(
            "span",
            class_="sc-7909e12c-0 glSvLE",
        )
        if pub_date_tag is None:
            return "Дата не установлена"

        pub_date = dateparser.parse(pub_date_tag.text)

        return pub_date.strftime("%Y-%m-%d")

    @staticmethod
    def is_tender_price_taken(card: Tag | Element) -> str:

        if isinstance(card, Element):
            return "Не установлено"

        price_tag = card.find(
            "div",
            class_="sc-a6b34174-0 cLruXa",
        )

        if price_tag is None:
            return "Не установлено"

        return price_tag.text.replace(',', ' ')

    @staticmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return 'Отсутствует'

        organize_tag = card.find(
            "div",
            class_="sc-6c01eeae-10 hqcmWX",
        )

        if organize_tag is None:
            return "Отсутствует"

        organize_text = organize_tag.text.replace(
            "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ",
            "ООО",
        ).replace(
            "общество с ограниченной ответственностью",
            "ООО",
        )

        return organize_text

    @staticmethod
    def get_end_date(card: Tag | Element) -> str | date:
        if isinstance(card, Element):
            return "Дата не установлена"

        end_date = card.find(
            "span",
            class_="sc-7909e12c-0 glSvLE",
        )

        if end_date is None:
            return "Дата не установлена"

        pub_date = dateparser.parse(end_date.text)

        return pub_date.date()

    @staticmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        return {
            "name": key_word,
            "status[]": "Приём заявок",
        }

    def get_cards_data(self) -> ResultSet[Tag]:
        soup = BeautifulSoup(self.html_source, "html.parser")
        return soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc")
