# scraper/infrastructure/parsing/date/html_parsers/meta_extractor.py
from __future__ import annotations
from typing import Optional, Tuple
from bs4 import BeautifulSoup
from scraper.domain.ports import DateExtractor

DATE_META_SELECTORS: list[Tuple[str, dict[str, str]]] = [
    ("meta", {"property": "article:published_time"}),
    ("meta", {"name": "article:published_time"}),
    ("meta", {"property": "og:published_time"}),
    ("meta", {"itemprop": "datePublished"}),
    ("meta", {"name": "pubdate"}),
]

class MetaDateExtractor:
    name = "meta"

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        for tag, attrs in DATE_META_SELECTORS:
            el = soup.find(tag, attrs)
            if not el:
                continue
            content = (el.get("content") or "").strip()
            if content:
                return content
        return None
