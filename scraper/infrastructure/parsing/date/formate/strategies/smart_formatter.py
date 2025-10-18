# infrastructure/parsing/date/formatters/smart_formatter.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True, slots=True)
class SmartFormatter:
    name: str = "smart"

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            self.log.debug("Pominięto formatowanie 'smart': pusty tekst wejściowy.")
            return None
        try:
            import dateparser
            dt = dateparser.parse(
                text.strip(),
                languages=["pl"],
                settings={
                    "PREFER_DATES_FROM": "past",
                    "RETURN_AS_TIMEZONE_AWARE": True,
                    "TIMEZONE": "Europe/Warsaw",
                    "TO_TIMEZONE": "Europe/Warsaw",
                },
            )
            if dt:
                self.log.info('Sparsowano datę przy użyciu dateparser (iso="%s").', dt.isoformat())
            else:
                self.log.debug('Nie rozpoznano daty przez dateparser (próbka="%s").', str(text)[:80])
            return dt
        except Exception:
            self.log.error("Błąd podczas formatowania 'smart' (dateparser).", exc_info=True)
            return None