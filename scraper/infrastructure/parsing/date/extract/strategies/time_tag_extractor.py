# scraper/infrastructure/parsing/date/html_parsers/time_tag_extractor.pyfrom __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.strategies.utils import _safe_str_strip


@dataclass(frozen=True, slots=True)
class TimeTagDateExtractor:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            times = soup.find_all("time") or []
        except Exception:
            self.log.error('Błąd podczas wyszukiwania tagów <time>.', exc_info=True)
            return None

        for t in times:
            try:
                raw = _safe_str_strip(t.get("datetime")) or _safe_str_strip(t.get_text(" ", strip=True))
            except Exception:
                self.log.error("Błąd podczas odczytu zawartości z tagu <time>.", exc_info=True)
                continue

            if raw:
                self.log.info('Wyodrębniono datę z tagu <time> (len=%d, próbka="%s").', len(raw), raw[:120])
                return raw

        self.log.debug("Nie znaleziono wartości daty w tagach <time>.")
        return None