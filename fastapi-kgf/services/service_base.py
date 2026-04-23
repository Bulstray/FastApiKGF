from sqlalchemy.ext.asyncio.session import AsyncSession

from storage.db.base_crud import BaseCRUD

from core.types.model import Model


class BaseService:
    """Base class for abstract repositories."""

    def __init__(self, session: AsyncSession, model: Model) -> None:
        """Initialize the repository with a database connection."""
        self.session = session
        self.base_crud: BaseCRUD = BaseCRUD(
            session=self.session,
            model=model,
        )

    async def get_by_id(self, id_: int) -> Model | None:
        return await self.base_crud.get_by_id(id_)

    async def get_all(self):
        """Get all records from table"""
        return await self.base_crud.get_all()

    async def delete_by_id(self, id_: int) -> None:
        """Delete record from table"""
        await self.base_crud.delete_by_id(id_)

    async def create(self, model: Model):
        """Create a new record in DB"""
        return await self.base_crud.create(model)
