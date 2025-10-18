# scraper/infrastructure/parsing/date/html_parsers/class_based_extractor.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup
from scraper.domain.ports import DateExtractor

SELECTOR = '[class*="date"], [class*="time"], .post-meta, .entry-meta'

@dataclass(frozen=True, slots=True)
class ClassBasedDateExtractor:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            elements = soup.select(SELECTOR) or []
        except Exception:
            self.log.error("Błąd podczas selekcji elementów (SELECTOR=%r).", SELECTOR, exc_info=True)
            return None

        for el in elements:
            try:
                raw = el.get_text(" ", strip=True)
            except Exception:
                self.log.error("Błąd podczas odczytu tekstu z elementu.", exc_info=True)
                continue

            if raw:
                self.log.info('Wyodrębniono tekst daty z elementu (len=%d, próbka="%s").', len(raw), raw[:120])
                return raw

        self.log.debug("Nie znaleziono tekstu daty w elementach dopasowanych przez SELECTOR.")
        return None