from pydantic import ConfigDict

from .base import MessageBase


class MessageCreate(MessageBase):
    """A model for storing messages"""

    model_config = ConfigDict(extra="ignore")
