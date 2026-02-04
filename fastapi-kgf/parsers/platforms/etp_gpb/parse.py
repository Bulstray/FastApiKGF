from datetime import datetime
from xml.etree.ElementTree import Element

from bs4 import Tag
from defusedxml import ElementTree

from core.config import settings
from parsers.platforms.base_platform import BaseTenderPlatform


class EtpgpbParser(BaseTenderPlatform):
    """Parser for ETP GPB tender platform."""

    def __init__(self, key_word: str) -> None:
        super().__init__(
            base_url=f"{settings.tender_platform.etp_gpb}",
            params=self.get_params(key_word=key_word),
        )

    @staticmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        return {"search": key_word}

    @staticmethod
    def is_tender_name_taken(card: Element | Tag) -> str:
        name_tag = card.find("title")
        if name_tag is None:
            return "Имя не найдено"
        return f"{name_tag.text}"

    @staticmethod
    def is_tender_pub_date_taken(card: Element | Tag) -> str:
        pub_date_tag = card.find("pubDate")

        if pub_date_tag is None:
            return "Дата не найдена"

        if not pub_date_tag.text:
            return "Дата не найдена"

        pub_date_str = datetime.strptime(
            pub_date_tag.text,
            "%a, %d %b %Y %H:%M:%S %z",
        )

        return pub_date_str.strftime("%Y-%m-%d")

    def get_cards_data(self) -> list[Element]:
        root = ElementTree.fromstring(self.response.text)
        return root.findall(".//item")
