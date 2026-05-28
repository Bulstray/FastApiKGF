import json

from services import (
    KeyWordService,
    TendersService,
    ArchiveTendersService,
    UserService,
)

from core.models import db_helper
from core.schemas import TenderCreate
from tasks.new_tender_notification import send_new_tenders_email

from typing import cast

import aiohttp


async def parse_tenders() -> None:
    async with db_helper.session_factory() as session:
        keyword_service = KeyWordService(session)
        tender_service = TendersService(session)
        tender_archive_service = ArchiveTendersService(session)
        user_service = UserService(session)

        all_users = cast(
            "list[User]",
            await user_service.get_all(),
        )

        all_keywords = cast(
            "list[ParsingKeyword]",
            await keyword_service.get_all(),
        )

        active_tenders = cast(
            "list[Tender]",
            await tender_service.get_all(),
        )

        if active_tenders:
            await tender_archive_service.add_all_from_active_tender(
                active_tenders,
            )
            await tender_service.delete_table()

        tenders = []
        tender_for_send = []

        for keyword in all_keywords:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:8002/api/v1/tenders/{keyword.keyword}/{keyword.id}"
                ) as response:
                    api_tenders = json.loads(await response.text())

            tenders.extend(
                [TenderCreate.model_validate(tender) for tender in api_tenders]
            )

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
                        await send_new_tenders_email.kiq(
                            user.email,
                            tender_for_send,
                        )
                        for user in all_users
                        if user.settings and user.settings.tender_notification
                    ]
            except Exception as e:
                print(e)

            await tender_service.add_tenders_in_db(tenders)
