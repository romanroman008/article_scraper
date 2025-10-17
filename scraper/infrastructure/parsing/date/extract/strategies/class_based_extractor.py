# scraper/infrastructure/parsing/date/html_parsers/class_based_extractor.py
from __future__ import annotations
from typing import Optional
from bs4 import BeautifulSoup
from scraper.domain.ports import DateExtractor

SELECTOR = '[class*="date"], [class*="time"], .post-meta, .entry-meta'

class ClassBasedDateExtractor:
    name = "class-based"

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        for el in soup.select(SELECTOR):
            raw = el.get_text(" ", strip=True)
            if raw:
                return raw
        return None
