from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import unicodedata

from scraper.infrastructure.parsing.date.parser_chain import TZ
from scraper.infrastructure.parsing.date.strategies.polish_patterns import RX_DDMMYYYY, RX_PL_WORDS, PL_MONTHS


@dataclass(frozen=True)
class PolishParser:
    """„Twardy” parser polskich formatów: 'dd.mm.yyyy' oraz 'd <miesiąc> yyyy'."""
    name: str = "pl-hard"

    def parse(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = unicodedata.normalize("NFKC", text).strip()

        m = RX_DDMMYYYY.search(s)
        if m:
            d, mo, y = map(int, m.groups())
            return datetime(y, mo, d, 0, 0, 0, tzinfo=TZ)

        m = RX_PL_WORDS.search(s.lower())
        if m:
            d = int(m.group(1))
            month_word = m.group(2)
            y = int(m.group(3))
            mo = PL_MONTHS.get(month_word)
            if mo:
                return datetime(y, mo, d, 0, 0, 0, tzinfo=TZ)

        return None
