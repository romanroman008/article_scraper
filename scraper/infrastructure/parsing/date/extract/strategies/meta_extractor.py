
from __future__ import annotations

import logging
from typing import Optional, Tuple
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.strategies.utils import _safe_str_strip

DATE_META_SELECTORS: list[Tuple[str, dict[str, str]]] = [
    ("meta", {"property": "article:published_time"}),
    ("meta", {"name": "article:published_time"}),
    ("meta", {"property": "og:published_time"}),
    ("meta", {"itemprop": "datePublished"}),
    ("meta", {"name": "pubdate"}),
]

class MetaDateExtractor:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            for tag, attrs in DATE_META_SELECTORS:
                if not isinstance(attrs, dict):
                    self.log.debug(
                        "Pominięto selektor meta: nieprawidłowe 'attrs' (tag=%s).", tag
                    )
                    continue

                el = soup.find(tag, attrs)
                if not el:
                    continue

                content = _safe_str_strip(el.get("content"))
                if content:
                    self.log.info(
                        'Wyodrębniono datę z meta (tag=%s, klucze=%s, długość=%d, próbka="%s").',
                        tag,
                        ",".join(list(attrs.keys())[:3]) if attrs else "",
                        len(content),
                        content[:120],
                    )
                    return content

            # nic nie zwrócono w pętli
            self.log.debug("Nie znaleziono daty w tagach meta (brak atrybutu 'content').")
            return None

        except Exception:
            self.log.error("Błąd podczas ekstrakcji daty z tagów meta.", exc_info=True)
            return None


