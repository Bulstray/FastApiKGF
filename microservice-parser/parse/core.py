from .platform import TekTorgPlatform, EtpgpbParser


class TenderParseCore:
    def __init__(
        self,
        key_word: str,
        keyword_id: int,
    ) -> None:
        self.parsers = {
            TekTorgPlatform(key_word, keyword_id),
            EtpgpbParser(key_word, keyword_id),
        }

    def search_all_platforms(self) -> list:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            results.extend(parse_class.search_tenders())


        return results