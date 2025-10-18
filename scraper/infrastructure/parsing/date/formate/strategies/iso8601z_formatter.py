# infrastructure/parsing/date/formatters/iso8601z_formatter.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

ISO_RX = re.compile(
    r"^\s*\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+\-]\d{2}:\d{2})\s*$"
)

@dataclass(frozen=True, slots=True)
class ISO8601ZFormatter:
    name: str = "iso8601z"

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            self.log.debug("Pominięto formatowanie ISO8601: pusty tekst wejściowy.")
            return None

        s = str(text).strip()
        if not ISO_RX.match(s):
            self.log.debug('Nie rozpoznano formatu ISO8601 (próbka="%s").', s[:60])
            return None

        s = s.replace(",", ".")
        if s.endswith(("Z", "z")):
            s = s[:-1] + "+00:00"
        if " " in s and "T" not in s[:20]:
            s = s.replace(" ", "T", 1)

        try:
            dt = datetime.fromisoformat(s)
            self.log.info('Sparsowano datę w formacie ISO8601 (iso="%s").', dt.isoformat())
            return dt
        except ValueError:
            self.log.debug('Nie udało się sparsować ISO8601 (fromisoformat, próbka="%s").', s[:60])
            return None
        except Exception:
            self.log.error("Błąd podczas formatowania ISO8601.", exc_info=True)
            return None