from pydantic import BaseModel

from core.types.platform import Platform


class BaseTender(BaseModel):
    """The base model for tenders"""
    platform: Platform
    name: str
    pub_date: str


class Tender(BaseTender):
    """A model for data storage"""
