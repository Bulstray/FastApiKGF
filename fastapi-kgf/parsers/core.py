from core.schemas import Tender

from .platforms import EtpgpbParser, TekTorgPlatform

from services.tenders.key_word_service import KeyWordService
from services.tenders.tender_service import TendersService
from core.models import db_helper


class TenderParseCore:
    def __init__(
        self,
        key_word: str,
        keyword_id: int,
    ) -> None:
        self.parsers = {
            TekTorgPlatform(key_word, keyword_id),
            EtpgpbParser(
                key_word,
                keyword_id,
            ),
        }

    def search_all_platforms(self) -> list[Tender]:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            results.extend(parse_class.search_tenders())

        return results


async def parse_tenders():
    async with db_helper.session_factory() as session:
        keyword_service = KeyWordService(session)
        tender_service = TendersService(session)

        all_keywords = await keyword_service.get_all()

        for keyword in all_keywords:
            tender_parser = TenderParseCore(
                keyword.keyword,
                keyword.id,
            )

            tenders = tender_parser.search_all_platforms()

        await tender_service.add_tenders_in_db(tenders)
