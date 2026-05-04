from pydantic import BaseModel
from datetime import date


class BaseTender(BaseModel):
    """The base model for tenders"""

    name: str
    pub_date: str
    price: str
    organizer: str
    url: str
    end_date: str
    keyword_id: int


class Tender(BaseTender):
    """A model for data storage"""
