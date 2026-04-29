from core.schemas import Tender
from core.types.platform import Platform

from .platforms import EtpgpbParser, TekTorgPlatform


class TenderParseCore:
    def __init__(self, key_word: str) -> None:
        self.parsers = {
            (TekTorgPlatform(key_word=key_word)),
        }

    def search_all_platforms(self) -> list[Tender]:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            results.extend(parse_class.search_tenders())

        return results
