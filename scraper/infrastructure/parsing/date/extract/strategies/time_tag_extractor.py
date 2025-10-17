# scraper/infrastructure/parsing/date/html_parsers/time_tag_extractor.py
from __future__ import annotations
from typing import Optional
from bs4 import BeautifulSoup
from scraper.domain.ports import DateExtractor

class TimeTagDateExtractor:
    name = "time-tag"

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        for t in soup.find_all("time"):
            raw = (t.get("datetime") or t.get_text(" ", strip=True) or "").strip()
            if raw:
                return raw
        return None
