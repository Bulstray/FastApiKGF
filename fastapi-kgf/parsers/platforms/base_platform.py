from abc import ABC, abstractmethod
from pydantic import AnyUrl


class BaseTenderPlatform(ABC):
    """Базовый класс для всех парсеров площадок"""

    def __init__(self, base_url: AnyUrl) -> None:
        self.base_url = base_url

    @abstractmethod
    def search_tenders(self, key_word: str):
        """Поиск тендеров по ключевому слову"""
        pass
