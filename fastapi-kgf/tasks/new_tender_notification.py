from malling.send_new_tender import send_new_tenders
from core.schemas import TenderCreate
from core import broker

import logging

log = logging.getLogger(__name__)


@broker.task
async def send_new_tenders_email(
    recipient: str,
    subject: list[TenderCreate],
) -> None:
    log.info(f"Sending new tenders to %s", recipient)
    await send_new_tenders(recipient, subject)
