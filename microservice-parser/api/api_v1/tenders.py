from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from parse.core import TenderParseCore

from core.config import settings

router = APIRouter(prefix=settings.api.v1.tenders)


@router.get("/{keyword}/{keyword_id}")
async def get_active_tenders_for_key_word(
    parse_core: Annotated[TenderParseCore, Depends(TenderParseCore)],
) -> list[dict[str, datetime | str | None | int]]:
    return parse_core.search_all_platforms()
