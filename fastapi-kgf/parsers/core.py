from core.models import db_helper
from core.schemas import TenderCreate
from services import (
    ArchiveTendersService,
    KeyWordService,
    TendersService,
    UserService,
)
from tasks import send_new_tenders_email

from .platforms import EtpgpbParser, TekTorgPlatform


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

    def search_all_platforms(self) -> list[TenderCreate]:
        """Поиск по всем платформам"""

        results = []

        for parse_class in self.parsers:
            try:
                results.extend(parse_class.search_tenders())
            except Exception:
                continue

        return results


async def parse_tenders():
    async with db_helper.session_factory() as session:
        keyword_service = KeyWordService(session)
        tender_service = TendersService(session)
        tender_archive_service = ArchiveTendersService(session)
        user_service = UserService(session)

        all_users = await user_service.get_all()

        all_keywords = await keyword_service.get_all()
        active_tenders = await tender_service.get_all()

        if active_tenders:
            await tender_archive_service.add_all_from_active_tender(
                active_tenders,
            )
            await tender_service.delete_table()

        tenders = []
        tender_for_send = []

        for keyword in all_keywords:
            tender_parser = TenderParseCore(
                keyword.keyword,
                keyword.id,
            )

            tenders.extend(tender_parser.search_all_platforms())

        for tender in tenders:
            archive_tender = await tender_service.get_archive_tender(
                tender.url,
            )
            if archive_tender:
                await tender_archive_service.delete(archive_tender)
            else:
                tender_for_send.append(tender)

        if tenders:
            try:
                if tender_for_send:
                    [
                        await send_new_tenders_email.kiq(user.email, tender_for_send)
                        for user in all_users
                        if user.settings and user.settings.tender_notification
                    ]
            except Exception as e:
                print(e)

            await tender_service.add_tenders_in_db(tenders)
