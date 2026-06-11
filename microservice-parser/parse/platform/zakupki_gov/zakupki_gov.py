from datetime import datetime
from typing import cast
from xml.etree.ElementTree import Element

import dateparser
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from core.config import settings
from parse.platform.base_platform import BaseTenderPlatform

from .zakupki_gov_fetcher import page_fetcher


class ZakupkiGovPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(self, key_word: str, keyword_id: int) -> None:
        source_html = page_fetcher(key_word)

        super().__init__(
            base_platform=f"{settings.platforms.base_platform.base_tek_torg}",
            keyword_id=keyword_id,
            page_source=source_html,
        )

    @staticmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:

        title_block = card.find(
            'div',
            string='Размещено',
        )
        if title_block:
            parent_block = title_block.find_parent('div', class_='col-6')
            value_block = parent_block.find('div', class_='data-block__value')
            return value_block.text.strip()
        else:
            return "Дата не установлена"

    def is_tender_name_taken(
        self,
        card: Tag | Element,
    ) -> tuple[str, str] | None:

        if isinstance(card, Element):
            return None

        name_tag = card.find(
            "div",
            class_="registry-entry__body-value",
        )

        if name_tag is None:
            return None

        url_tag = card.find("a").get("href")

        return f"{name_tag.text}", f"{url_tag}"

    def get_cards_data(self) -> ResultSet[Tag]:
        soup = BeautifulSoup(self.html_source, "html.parser")
        return soup.find_all(
            "div",
            class_="row no-gutters registry-entry__form mr-0",
        )
