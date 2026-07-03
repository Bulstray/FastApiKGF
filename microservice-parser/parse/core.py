from datetime import datetime
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException
from .platform import EtpgpbParser, SberPlatform, TekTorgPlatform, LukhoilPlatform
from .platform.sber.sber_fetcher import page_fetcher as sber_page_fetcher
from .platform.tek_torg.tek_torg_fetcher import page_fetcher as tek_torg_page_fether
from .platform.etp_gpb.etp_gpb_fetcher import page_fetcher as etp_gpb_page_fecher
from .platform.lukh.lukh_fetch import page_fetcher as lukh_page_fetcher
import logging

logger = logging.getLogger(__name__)


class TenderParseCore:
    def __init__(
        self,
        keyword: str,
        keyword_id: int,
    ) -> None:
        self.keyword = keyword
        self.keyword_id = keyword_id
        self.parsers = {
            (TekTorgPlatform, tek_torg_page_fether),
            (EtpgpbParser, etp_gpb_page_fecher),
            (SberPlatform, sber_page_fetcher),
            (LukhoilPlatform, lukh_page_fetcher),
        }

    def search_all_platforms(self) -> list[dict[str, str | datetime | int | None]]:
        """Поиск по всем платформам"""

        results = []

        for parse_platform, page_fetcher in self.parsers:
            try:
                source_html = page_fetcher(self.keyword)
                if source_html is None:
                    continue

                parse_class = parse_platform(self.keyword_id, source_html)
                tenders = parse_class.search_tenders()

            except SessionNotCreatedException as error:
                logger.error("Не удалось создать сессию Chrome: %s", str(error))
                logger.debug("Детали ошибка", exc_info=True)


            except Exception as e:
                print(e)
            else:
                results.extend(tenders)

        return results
