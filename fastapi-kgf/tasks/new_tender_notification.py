import logging

from core import broker
from core.schemas import TenderCreate
from malling.send_new_tender import send_new_tenders

log = logging.getLogger(__name__)


@broker.task
async def send_new_tenders_email(
    recipient: str,
    subject: list[TenderCreate],
) -> None:
    log.info("Sending new tenders to %s", recipient)
    await send_new_tenders(recipient, subject)
