from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from core.models import db_helper
from services import KeyWordService


class KeyWordFactory(KeyWordService):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ):
        super().__init__(session)
