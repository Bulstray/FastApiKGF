from .platforms import TekTorgPlatform, EtpgpbParser


class TenderParseCore:
    def __init__(self) -> None:
        self.parsers = {
            "tek_torg": TekTorgPlatform(),
            "etp_gpb": EtpgpbParser(),
        }

    def search_all_platforms(self, key_word: str):
        """Поиск по всем платформам"""

        results = []

        for platform_name, parse_class in self.parsers.items():
            results.extend(parse_class.search_tenders(key_word=key_word))

        return results


tender_parse_core = TenderParseCore()
