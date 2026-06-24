__all__ = ("broker",)

import logging

from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from core.config import settings

log = logging.getLogger(__name__)

broker = AioPikaBroker(
    url=f"{settings.taskiq.url}",
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.info("Worker startup completed, got state %s", state)
