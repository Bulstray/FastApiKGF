from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.types.model import Model


class BaseCRUD:
    """Base CRUD class for all models"""

    def __init__(self, session: AsyncSession, model: Model) -> None:
        """
        Initialize the base CRUD with a database connection and an ORM object.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session for database interaction.
            model (Model): ORM model class to work with.
        """
        self.session = session
        self.model = model

    async def get_by_id(self, id_: int) -> Model | None:
        """
        Get a model instance by its ID.

        Args:
            id_ (int): The ID of the model to retrieve.

        Returns:
            Model | None: The model instance if found, otherwise None.
        """
        return await self.session.get(self.model, id_)

    async def get_all(self) -> list[Model]:
        """
        Get all rows from the table, ordered by ID.

        Returns:
            list[Model]: List of all model instances in the table.
        """
        stmt = select(self.model).order_by(self.model.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def delete_by_id(self, id_: int) -> None:
        """Delete by id"""
        model = await self.get_by_id(id_)
        await self.delete(model)

    async def delete(self, model: Model) -> None:
        await self.session.delete(model)
        await self.session.commit()

    async def create(self, model: Model) -> Model:
        """Create new row in db"""
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
