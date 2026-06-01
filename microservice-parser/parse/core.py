from datetime import datetime

from .platform import EtpgpbParser, SberPlatform, TekTorgPlatform, LukhoilPlatform


class TenderParseCore:
    def __init__(
        self,
        keyword: str,
        keyword_id: int,
    ) -> None:
        self.keyword = keyword
        self.keyword_id = keyword_id
        self.parsers = {
            TekTorgPlatform,
            EtpgpbParser,
            SberPlatform,
            LukhoilPlatform,

        }

    def search_all_platforms(self) -> list[dict[str, str | datetime | int | None]]:
        """Поиск по всем платформам"""

        results = []

        for parse_platform in self.parsers:
            try:
                parse_class = parse_platform(self.keyword, self.keyword_id)
                tenders = parse_class.search_tenders()
            except Exception as e:
                print(e)
            else:
                results.extend(tenders)

        return results
