from datetime import datetime

from parsers.platforms.base_platform import BaseTenderPlatform

from core.config import settings
import requests

from xml.etree import ElementTree


class EtpgpbParser(BaseTenderPlatform):
    def __init__(self):
        super().__init__(base_url=settings.tender_platform.etp_gpb)

    def search_tenders(self, key_word: str):
        response = requests.get(f"{settings.tender_platform.etp_gpb}{key_word}")
        root = ElementTree.fromstring(response.content)

        tenders = []

        for tender in root.findall(".//item"):
            str_date = tender.find("pubDate").text
            date_datetime = datetime.strptime(str_date, "%a, %d %b %Y %H:%M:%S %z")

            tenders.append(
                {
                    "platform": "GAZP",
                    "name": tender.find("title").text,
                    "date": date_datetime.strftime("%Y-%m-%d"),
                }
            )
        return tenders
