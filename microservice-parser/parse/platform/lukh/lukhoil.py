from datetime import datetime
from xml.etree.ElementTree import Element

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from core.config import settings
from parse.platform.base_platform import BaseTenderPlatform

from .lukh_fetch import page_fetcher

import re


class LukhoilPlatform(BaseTenderPlatform):
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
        return soup.find_all(
            "div", class_="panel-default panel-collapsible panel-tender"
        )

    def is_tender_name_taken(
        self,
        card: Tag | Element,
    ) -> tuple[str, str] | None:

        if isinstance(card, Element):
            return None

        name_tag = card.find("h2")

        if name_tag is None:
            return None

        url = card.find("a", class_="button")

        if url is None:
            return None

        return f"{name_tag.text}", f"{url.get('href')}"

    @staticmethod
    def is_tender_price_taken(card: Tag | Element) -> str:
        return "Не установлено"

    @staticmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return "Отсутствует"

        organize_tag = card.find(
            'span',
            {'data-bind': 'text: Organization.Name'},
        )

        if organize_tag is None:
            return "Отсутствует"

        return organize_tag.text

    @staticmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:
        return "Дата не найдена"

    @staticmethod
    def get_end_date(card: Tag | Element) -> datetime | None:
        if isinstance(card, Element):
            return None

        end_card_div = card.find(
            'span',
            {'data-bind': re.compile(r'moment\(DateFinish\)\.format')},
        )
        end_date = datetime.strptime(end_card_div.text, "%d.%m.%Y")

        return end_date
