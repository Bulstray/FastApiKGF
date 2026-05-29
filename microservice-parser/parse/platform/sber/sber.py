from datetime import datetime

from parse.platform.base_platform import BaseTenderPlatform
from core.config import settings
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from xml.etree.ElementTree import Element

from .sber_fetcher import page_fetcher


class SberPlatform(BaseTenderPlatform):
    def __init__(self, key_word: str, keyword_id: int):
        source_html = page_fetcher(key_word)
        self.keyword = key_word.lower()
        super().__init__(
            base_platform=settings.platforms.sber,
            keyword_id=keyword_id,
            page_source=source_html,
        )

    def get_cards_data(self) -> ResultSet[Tag]:
        soup = BeautifulSoup(self.html_source, "html.parser")
        return soup.find_all("tbody")

    def is_tender_name_taken(
        self,
        card: Tag | Element,
    ) -> tuple[str, str] | None:

        if isinstance(card, Element):
            return None

        name_tag = card.find("span", class_="es-el-name")

        if name_tag is None or self.keyword not in name_tag.text.lower():
            return None

        number = card.find("span", class_="es-el-code-term")

        if number is None:
            return None

        return f"{name_tag.text}", f"{number.text}"

    @staticmethod
    def is_tender_price_taken(card: Tag | Element) -> str:

        if isinstance(card, Element):
            return "Не установлено"

        price_tag = card.find(
            "span",
            class_="es-el-amount",
        )

        if price_tag is None:
            return "Не установлено"

        return price_tag.text

    @staticmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return "Отсутствует"

        organize_tag = card.find(
            "div",
            class_="es-el-org-name",
        )

        if organize_tag is None:
            return "Отсутствует"

        return organize_tag.text

    @staticmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:

        if isinstance(card, Element):
            return "Дата не найдена"

        pub_date_tag = card.find(
            "span",
            attrs={"content": "leaf:PublicDate"},
        )

        if pub_date_tag is None:
            return "Дата не установлена"

        pub_date = datetime.strptime(pub_date_tag.text, "%d.%m.%Y %H:%M")
        return pub_date.strftime("%Y-%m-%d")

    @staticmethod
    def get_end_date(card: Tag | Element) -> datetime | None:
        if isinstance(card, Element):
            return None

        end_card_div = card.find(
            "span",
            attrs={"content": "leaf:RequestDate"},
        )

        end_date = datetime.strptime(end_card_div.text, "%d.%m.%Y %H:%M")

        return end_date
