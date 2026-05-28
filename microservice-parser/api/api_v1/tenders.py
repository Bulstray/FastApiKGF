from fastapi import APIRouter, Depends

from typing import Annotated

from core.config import settings
from parse.core import TenderParseCore

router = APIRouter(prefix=settings.api.v1.tenders)


@router.get("/{keyword}/{keyword_id}")
async def get_active_tenders_for_key_word(
    parse_core: Annotated[TenderParseCore, Depends(TenderParseCore)],
):
    return parse_core.search_all_platforms()
