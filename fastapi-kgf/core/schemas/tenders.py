from pydantic import BaseModel

from core.types.platform import Platform


class BaseTender(BaseModel):
    platform: Platform
    name: str
    pub_date: str


class Tender(BaseTender):
    """Модель для хранения данных о тенедере"""
