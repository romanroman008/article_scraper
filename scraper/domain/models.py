# scraper/domain/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ArticleData:
    url: str
    title: str
    content_html: str
    content_text: str
    published_at: str
    source_domain: str
    raw_date: str
    new:str
