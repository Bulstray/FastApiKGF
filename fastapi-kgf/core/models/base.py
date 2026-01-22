from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(input_str=cls.__name__)}"
