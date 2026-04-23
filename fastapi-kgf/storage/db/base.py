from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.types import Model


class BaseCRUD:
    """Base CRUD class for all models"""

    def __init__(self, session: AsyncSession, model: Model) -> None:
        """Initialize the base crud with a database connection and an ORM object."""
        self.session = session
        self.model = model

    async def get_by_id(self, id_: int) -> Model | None:
        """Get a model by its ID."""
        return await self.session.get(self.model, id_)

    async def get_all(self) -> list[Model]:
        """Get all rows from table"""
        stmt = select(self.model).order_by(self.model.id)
        result = await self.session.scalars(stmt)
        return list(result.all())
