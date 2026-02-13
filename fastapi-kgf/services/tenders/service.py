import json

from core.schemas import Tender
from parsers.core import TenderParseCore
from storage.redis import tenders as redis_tender


def get_tenders_by_keyword(keyword: str) -> list[Tender]:
    """
    Получает тендеры по ключевому слову.
    Сначала проверяет кеш Redis,
    при отсутствии данных парсит с платформ и кеширует.
    """
    normalized_keyword = keyword.lower()

    # Проверяем кеш
    cached_tenders_json = redis_tender.get_tenders(normalized_keyword)

    if cached_tenders_json is not None:
        return _parse_cached_tenders(cached_tenders_json)

    # Парсим новые тендеры и кешируем
    tenders = TenderParseCore(
        key_word=normalized_keyword,
    ).search_all_platforms()
    _cache_tenders(normalized_keyword, tenders)

    return tenders


def _parse_cached_tenders(cached_tenders_json: str) -> list[Tender]:
    """Преобразует закешированные тендеры из JSON в объекты Tender."""
    tenders_data = json.loads(cached_tenders_json)
    return [Tender.model_validate(tender_data) for tender_data in tenders_data]


def _cache_tenders(keyword: str, tenders: list[Tender]) -> None:
    """Кеширует тендеры в Redis."""
    tenders_json = json.dumps(
        [tender.model_dump() for tender in tenders],
    )
    redis_tender.save_tenders(key_word=keyword, tenders_str=tenders_json)
