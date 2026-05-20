from .base import MessageBase
from pydantic import ConfigDict


class MessageCreate(MessageBase):
    """A model for storing messages"""

    model_config = ConfigDict(extra="ignore")
