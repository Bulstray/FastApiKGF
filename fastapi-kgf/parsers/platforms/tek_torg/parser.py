from datetime import UTC, datetime
from xml.etree.ElementTree import Element

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from core.config import settings
from parsers.platforms.base_platform import BaseTenderPlatform


class TekTorgPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(self, key_word: str) -> None:
        super().__init__(
            base_url=f"{settings.tender_platform.tek_torg}",
            params=self.get_params(key_word=key_word),
        )

    @staticmethod
    def is_tender_name_taken(card: Tag | Element) -> str:
        name_tag = card.find("a")

        if name_tag is None:
            return "Имя не найдено"

        return f"{name_tag.text}"

    @staticmethod
    def is_tender_pub_date_taken(card: Tag | Element) -> str:

        if isinstance(card, Element):
            return "Дата не найдена"

        pub_date_tag = card.find(
            "span",
            class_="sc-7909e12c-0 glSvLE",
        )
        if pub_date_tag is None:
            return "Дата не найдена"

        pub_date = datetime.strptime(
            pub_date_tag.text,
            "%d.%m.%Y",
        ).replace(tzinfo=UTC)

        return pub_date.strftime("%Y-%m-%d")

    @staticmethod
    def get_params(key_word: str) -> dict[str, str | int]:
        return {
            "name": key_word,
            "status[]": "Приём заявок",
        }

    def get_cards_data(self) -> ResultSet[Tag]:
        soup = BeautifulSoup(self.response.text, "html.parser")
        return soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc")
