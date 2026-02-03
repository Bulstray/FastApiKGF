from bs4 import BeautifulSoup
from bs4.element import Tag

from datetime import datetime, date

from parsers.platforms.base_platform import BaseTenderPlatform
import requests
from core.config import settings


class TekTorgPlatform(BaseTenderPlatform):
    """Парсер площадки ТЕК-Торг"""

    def __init__(self):
        super().__init__(base_url=settings.tender_platform.tek_torg)

    def search_tenders(self, key_word: str):
        """Поиск тендеров на ТЕК-Торг"""
        response = requests.get(f"{self.base_url}{key_word}")

        soup = BeautifulSoup(response.text, "html.parser")

        tender_cards = soup.find_all("div", class_="sc-6c01eeae-0 jtfzxc")

        date_now = datetime.now().date()

        tenders = []
        for card in tender_cards:
            deadline = self.get_deadline(card=card)

            if date_now > deadline:
                continue

            tenders.append(
                {
                    "platform": "ROSH",
                    "name": card.find("a").text,
                    "date": deadline.strftime("%Y-%m-%d"),
                }
            )
        return tenders

    @staticmethod
    def get_deadline(card: Tag) -> date:
        deadline = (
            card.find("time", class_="sc-7909e12c-2 fIvbdF")
            .find("span", class_="sc-7909e12c-0 glSvLE")
            .text
        )

        return datetime.strptime(deadline, "%d.%m.%Y").date()
