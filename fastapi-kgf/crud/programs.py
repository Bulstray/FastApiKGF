from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models import Program


def get_all_programs(
    session: Session,
) -> Sequence[Program]:
    stmt = select(Program).order_by(Program.id)
    result = session.scalars(stmt)
    return result.all()
