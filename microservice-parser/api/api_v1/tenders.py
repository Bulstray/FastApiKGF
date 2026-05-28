from fastapi import APIRouter

from core.config import settings

router = APIRouter(prefix=settings.api.v1.tenders)


@router.get("/{keyword}/{keyword_id}")
async def get_active_tenders_for_key_word(keyword: str, keyword_id: int):
    return {"message": "Hello World"}
