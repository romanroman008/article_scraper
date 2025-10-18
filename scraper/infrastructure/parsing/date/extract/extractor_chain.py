import logging
from dataclasses import dataclass
from typing import Optional, Sequence

from bs4 import BeautifulSoup

from scraper.domain.ports import DateExtractor


@dataclass(frozen=True, slots=True)
class DateExtractorChain:
    parsers: Sequence["DateExtractor"]

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        """Próbuje kolejno ekstraktorów, aż jeden zwróci wynik."""
        try:
            tried: list[str] = []
            for parser in self.parsers:
                name = getattr(parser, "name", parser.__class__.__name__)
                tried.append(name)

                result = parser.extract(soup)
                if result and str(result).strip():
                    val = str(result).strip()
                    self.log.info(
                        'Ekstrakcja daty zakończona powodzeniem (extractor=%s, próbka="%s").',
                        name,
                        val[:120],
                    )
                    return val

                self.log.debug("Brak dopasowania daty w ekstraktorze (extractor=%s).", name)

            self.log.debug("Żaden ekstraktor nie zwrócił daty (tried=%s).", ", ".join(tried))
            return None

        except Exception:
            self.log.error("Błąd podczas wykonywania łańcucha ekstraktorów daty.", exc_info=True)
            return None