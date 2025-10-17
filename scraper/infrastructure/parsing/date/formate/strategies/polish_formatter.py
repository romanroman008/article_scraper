# infrastructure/parsing/date/formatters/polish_hard_formatter.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re
import unicodedata
import pytz

PL_MONTHS = {
    "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6,
    "lipca": 7, "sierpnia": 8, "września": 9, "wrzesnia": 9,
    "października": 10, "pazdziernika": 10, "listopada": 11, "grudnia": 12,
}
RX_DDMMYYYY = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
RX_PL_WORDS = re.compile(r"\b(\d{1,2})\s+([A-Za-ząćęłńóśźż]+)\s+(\d{4})\b", re.IGNORECASE)

@dataclass(frozen=True)
class PolishHardFormatter:
    """„Twardy” formater polskich formatów: 'dd.mm.yyyy' oraz 'd <miesiąc> yyyy'.
       Zwraca datetime NAIVE (czas = 00:00:00); polityka łańcucha doda TZ/UTC."""
    name: str = "pl-hard"
    tz_name: str = "Europe/Warsaw"

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = unicodedata.normalize("NFKC", text).strip()

        m = RX_DDMMYYYY.search(s)
        if m:
            d, mo, y = map(int, m.groups())
            try:
                # NAIVE – łańcuch nada TZ i przerobi na UTC
                return datetime(y, mo, d, 0, 0, 0)
            except ValueError:
                return None

        m = RX_PL_WORDS.search(s.lower())
        if m:
            d = int(m.group(1))
            month_word = m.group(2)
            y = int(m.group(3))
            mo = PL_MONTHS.get(month_word)
            if mo:
                try:
                    return datetime(y, mo, d, 0, 0, 0)  # NAIVE
                except ValueError:
                    return None

        return None
