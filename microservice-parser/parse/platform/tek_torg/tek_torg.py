from datetime import datetime
from typing import cast
from xml.etree.ElementTree import Element

import dateparser
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from core.config import settings
from parse.platform.base_platform import BaseTenderPlatform

from .tek_torg_fetcher import page_fetcher


class TekTorgPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(
        self,
        keyword_id: int,
        source_html: str,
    ) -> None:

        super().__init__(
            base_platform=f"{settings.platforms.base_platform.base_tek_torg}",
            keyword_id=keyword_id,
            page_source=source_html,
        )

    def is_tender_name_taken(
        self,
        card: Tag | Element,
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

        pub_date = cast(
            "datetime",
            dateparser.parse(pub_date_tag.text),
        )

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

        return price_tag.text.replace(",", " ")

    @staticmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return "Отсутствует"

        organize_tag = card.find(
            "div",
            class_="sc-6c01eeae-10 hqcmWX",
        )

        if organize_tag is None:
            return "Отсутствует"

        return (
            organize_tag.text.replace(
                "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ",
                "ООО",
            )
            .replace(
                "общество с ограниченной ответственностью",
                "ООО",
            )
            .replace(
                "АКЦИОНЕРНОЕ ОБЩЕСТВО",
                "АО",
            )
            .replace(
                "Публичное акционерное общество",
                "ПАО",
            )
        )

    @staticmethod
    def get_end_date(card: Tag | Element) -> datetime | None:
        if isinstance(card, Element):
            return None

        end_card_div = card.find_all(
            "div",
            class_="sc-6c01eeae-18 kxxgLZ",
        )[-1]

        end_date = end_card_div.find(
            "span",
            class_="sc-7909e12c-0 glSvLE",
        )

        if end_date is None:
            return None

        return datetime.strptime(
            end_date.text,
            "%d.%m.%Y",
        )

    def get_cards_data(self) -> ResultSet[Tag]:
        soup = BeautifulSoup(self.html_source, "html.parser")
        return soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc")
