from pydantic import BaseModel

from core.types.platform import Platform


class BaseTender(BaseModel):
    """The base model for tenders"""

    name: str
    pub_date: str
    price: str
    organizer: str


class Tender(BaseTender):
    """A model for data storage"""
