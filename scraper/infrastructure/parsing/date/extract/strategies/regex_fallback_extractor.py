
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, ClassVar
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.const import RX_DDMMYYYY, RX_PL_WORDS


@dataclass(frozen=True, slots=True)
class RegexFallbackDateExtractor:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            text = (soup.get_text(" ", strip=True) or "").lower()
        except Exception:
            self.log.error("Błąd podczas pobierania tekstu dokumentu do dopasowania regex.", exc_info=True)
            return None

        text = text[:100_000]  # defensywny limit
        for rx in (RX_DDMMYYYY, RX_PL_WORDS):
            try:
                m = rx.search(text)
            except Exception:
                self.log.error("Błąd podczas dopasowania wyrażenia regularnego (regex=%r).", getattr(rx, "pattern", "?"), exc_info=True)
                continue

            if m:
                val = m.group(0)
                self.log.info('Wyodrębniono datę na podstawie wzorca (regex=%r, len=%d, próbka="%s").',
                              getattr(rx, "pattern", "?"), len(val), val[:120])
                return val

        self.log.debug("Nie znaleziono dopasowania daty żadnym z wzorców regex.")
        return None