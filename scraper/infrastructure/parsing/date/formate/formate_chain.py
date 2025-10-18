# application/formatter_chain.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import datetime, time

from scraper.domain.ports import DateFormatter
from scraper.infrastructure.parsing.date.const import TZ

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DateTimeFormatterChain:
    formatters: Sequence["DateFormatter"]

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def format(self, text: str) -> str:
        """Próbuje kolejno formatterów, aż jeden zwróci sformatowaną datę."""
        try:
            if not text or not str(text).strip():
                self.log.debug("Pominięto formatowanie: pusty tekst wejściowy.")
                return ""

            tried: list[str] = []
            for f in self.formatters:
                name = getattr(f, "name", f.__class__.__name__)
                tried.append(name)

                dt = f.format(text)
                if dt is not None:
                    out = format_to_string_with_set_datezone(dt)
                    self.log.info(
                        'Formatowanie daty zakończone powodzeniem (formatter=%s, iso="%s").',
                        name,
                        getattr(dt, "isoformat", lambda: "?")(),
                    )
                    return out

                self.log.debug("Brak dopasowania formatu daty (formatter=%s).", name)

            self.log.debug("Żaden formatter nie zwrócił wyniku (tried=%s, próbka=\"%s\").",
                           ", ".join(tried), str(text)[:80])
            return ""

        except Exception:
            self.log.error("Błąd podczas wykonywania łańcucha formatterów daty.", exc_info=True)
            return ""



def format_to_string_with_set_datezone(dt: datetime) -> str:

    if dt.tzinfo is None:
        dt = TZ.localize(dt)
    else:
        dt = dt.astimezone(TZ)

    # Jeśli brak czasu, ustaw 00:00:00
    if dt.time() == time(0, 0):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    return dt.strftime("%d.%m.%Y %H:%M:%S")