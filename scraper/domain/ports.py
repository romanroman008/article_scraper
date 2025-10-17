# scraper/domain/ports.py
from datetime import datetime
from typing import Protocol, Iterable, List, Optional
from .models import ArticleData

class HtmlFetcher(Protocol):
    def fetch(self, url: str) -> str: ...

class Renderer(Protocol):
    def render(self, url: str) -> str: ...

class ArticleParser(Protocol):
    def parse(self, url: str, html: str) -> ArticleData: ...

class ArticleRepository(Protocol):
    def exists(self, url: str) -> bool: ...
    def save(self, article: ArticleData) -> None: ...

class DateParser(Protocol):
    name: str
    def parse(self, text: str) -> Optional[datetime]: ...