from datetime import datetime

from .platform import EtpgpbParser, SberPlatform, TekTorgPlatform


class TenderParseCore:
    def __init__(
        self,
        keyword: str,
        keyword_id: int,
    ) -> None:
        self.parsers = {
            TekTorgPlatform(keyword, keyword_id),
            EtpgpbParser(keyword, keyword_id),
            SberPlatform(keyword, keyword_id),
        }

    def search_all_platforms(self) -> list[dict[str, str | datetime | int | None]]:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            try:
                tenders = parse_class.search_tenders()
            except Exception as e:
                print(e)
            else:
                results.extend(tenders)

        return results
