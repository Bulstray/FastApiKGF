from datetime import datetime
from typing import cast
from xml.etree.ElementTree import Element

import dateparser
from bs4 import BeautifulSoup, ResultSet, Tag

from core.config import settings
from parse.platform.base_platform import BaseTenderPlatform


class EtpgpbParser(BaseTenderPlatform):
    """Parser for ETP GPB tender platform."""

    def __init__(
        self,
        keyword: str,
        keyword_id: int,
        source_html: str,
    ) -> None:

        self.keyword = keyword

        super().__init__(
            base_platform=f"{settings.platforms.base_platform.base_etp_gpb}",
            keyword_id=keyword_id,
            page_source=source_html,
        )

    @staticmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        return {
            "page": 1,
            "per": 100,
            "procedure[stage][0]": "accepting",
            "search": key_word,
            "sort": "by_relevance",
        }

    def is_tender_name_taken(
        self,
        card: Element | Tag,
    ) -> tuple[str, str] | None:

        if isinstance(card, Element):
            return None

        name_tag = card.find(
            "a",
            class_="vTitle vTitle--1",
        )

        if name_tag is None or self.keyword not in name_tag.text.lower():
            return None
        return f"{name_tag.text}", f"{name_tag.get('href')}"

    @staticmethod
    def is_tender_pub_date_taken(card: Element | Tag) -> str:

        if isinstance(card, Element):
            return "Дата не установлена"

        pub_date_tag = card.find(
            "div",
            class_="procedureDateExpired__value",
        )

        if pub_date_tag is None:
            return "Дата не найдена"

        if not pub_date_tag.text:
            return "Дата не найдена"

        pub_date_str = cast(
            "datetime",
            dateparser.parse(
                pub_date_tag.text.replace("МСК", ""),
            ),
        )

        return pub_date_str.strftime("%Y-%m-%d")

    @staticmethod
    def is_tender_price_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return "Цена не установлена"

        price_tag = card.find(
            "div",
            class_="vTitle vTitle--2 cardBody__price",
        )

        if price_tag is None:
            return "Цена не установлена"

        price_tag_text = cast(
            "str",
            price_tag.text,
        )

        return price_tag_text.replace(",", " ")

    @staticmethod
    def is_tender_organize_taken(card: Tag | Element) -> str:
        if isinstance(card, Element):
            return "Отсутствует"

        for organize in card.find_all("div", class_="cardBody__infoItem"):
            organize_tag = organize.find(
                "div",
                class_="vTxt--faint2Weak",
            )

            if (
                isinstance(organize_tag, Element)
                and "Заказчики" in organize_tag.text
            ):
                return organize.find(
                    "div",
                    class_="cardBody__truncate",
                ).text

        return "Отсутствует"

    @staticmethod
    def get_end_date(card: Tag | Element) -> None | datetime:
        if isinstance(card, Element):
            return None

        end_date = card.find(
            "div",
            class_="procedureDateExpired__value",
        )

        if end_date is None:
            return None

        return cast(
            "datetime",
            dateparser.parse(
                end_date.text.replace("МСК", ""),
            ),
        )

    def get_cards_data(self) -> ResultSet[Tag]:
        root = BeautifulSoup(self.html_source, "html.parser")
        return root.find_all("div", class_="proceduresList__item")
