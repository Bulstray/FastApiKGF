from malling.send_email import send_email
from core.schemas import TaskRead
from core import broker

import logging

log = logging.getLogger(__name__)


@broker.task
async def send_new_task_email(
    recipient: str,
    subject: TaskRead,
) -> None:
    log.info("Sending new task to %s", f"{recipient}")
    await send_email(recipient, subject)
