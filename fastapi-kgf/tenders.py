import json

import aiohttp

from core.models import db_helper
from core.schemas import TenderCreate
from storage.db import (
    crud_arhive_tenders,
    crud_user,
    crud_keyword_tenders,
    crud_tenders,
)
from tasks.new_tender_notification import send_new_tenders_email


async def parse_tenders() -> None:
    async with db_helper.session_factory() as session:

        all_users = await crud_user.get_all_users(session)

        all_keywords = await crud_keyword_tenders.get_all_keywords_tender(
            session
        )

        active_tenders = await crud_tenders.get_all_active_tenders(session)

        tenders = []
        tender_for_send = []

        for keyword in all_keywords:
            async with aiohttp.ClientSession() as session_client:
                async with session_client.get(
                    f"http://localhost:8002/api/v1/tenders/{keyword.keyword}/{keyword.id}",
                ) as response:
                    api_tenders = json.loads(await response.text())

            tenders.extend(
                [
                    TenderCreate.model_validate(tender)
                    for tender in api_tenders
                ],
            )

        if active_tenders:
            await crud_arhive_tenders.add_all_from_active_tender(
                session,
                active_tenders,
            )
            await crud_tenders.clear_table(session)

        for tender in tenders:
            archive_tender = (
                await crud_arhive_tenders.get_archive_tender_by_url(
                    session,
                    tender.url,
                )
            )
            if archive_tender:
                await crud_arhive_tenders.delete_archive_tender(
                    session,
                    archive_tender,
                )
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

            await crud_tenders.add_tenders_in_db(session, tenders)
