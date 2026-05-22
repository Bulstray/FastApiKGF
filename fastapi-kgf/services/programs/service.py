from sqlalchemy.ext.asyncio import AsyncSession

from storage.db import ProgramsStorage


class ProgramService(ProgramsStorage):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session)
