# scraper/infrastructure/parsing/date/html_parsers/regex_fallback_extractor.py
from __future__ import annotations
from typing import Optional
from bs4 import BeautifulSoup
from scraper.domain.ports import DateExtractor
from scraper.infrastructure.parsing.date.strategies.polish_parser import RX_DDMMYYYY, RX_PL_WORDS


class RegexFallbackDateExtractor:
    name = "regex-fallback"

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        text = (soup.get_text(" ", strip=True) or "").lower()
        for rx in (RX_DDMMYYYY, RX_PL_WORDS):
            m = rx.search(text)
            if m:
                return m.group(0)
        return None

