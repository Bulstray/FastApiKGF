import logging

from core import broker
from core.schemas import TaskRead
from malling.send_email import send_email

log = logging.getLogger(__name__)


@broker.task
async def send_new_task_email(
    recipient: str,
    subject: TaskRead,
) -> None:
    log.info("Sending new task to %s", f"{recipient}")
    await send_email(recipient, subject)
