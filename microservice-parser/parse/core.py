from .platform import TekTorgPlatform, EtpgpbParser
from datetime import datetime


class TenderParseCore:
    def __init__(
        self,
        keyword: str,
        keyword_id: int,
    ) -> None:
        self.parsers = {
            TekTorgPlatform(keyword, keyword_id),
            EtpgpbParser(keyword, keyword_id),
        }

    def search_all_platforms(self) -> list[dict[str, str | datetime | int]]:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            results.extend(parse_class.search_tenders())


        return results