# application/formatter_chain.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import datetime, time

from scraper.domain.ports import DateFormatter
from scraper.infrastructure.parsing.date.const import TZ


@dataclass
class DateTimeFormatterChain:
    formatters: Sequence[DateFormatter]


    def format(self, text: str) -> str:
        if not text:
            return ""
        for f in self.formatters:
            dt = f.format(text)
            if dt is not None:
                return format_to_string_with_set_datezone(dt)
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