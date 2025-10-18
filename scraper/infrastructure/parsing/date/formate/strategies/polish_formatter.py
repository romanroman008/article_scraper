# infrastructure/parsing/date/formatters/polish_hard_formatter.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re
import unicodedata

PL_MONTHS = {
    "stycznia":1,"lutego":2,"marca":3,"kwietnia":4,"maja":5,"czerwca":6,
    "lipca":7,"sierpnia":8,"września":9,"wrzesnia":9,"października":10,"pazdziernika":10,
    "listopada":11,"grudnia":12
}

# dd.mm.yyyy [HH:MM[:SS]]
RX_NUMERIC = re.compile(
    r"\b(?P<d>\d{1,2})[.\-/](?P<m>\d{1,2})[.\-/](?P<y>\d{4})"
    r"(?:[ ,T]*(?:o\s+)?"                       # separator / "o "
    r"(?P<h>\d{1,2}):(?P<min>\d{2})(?::(?P<s>\d{2}))?)?\b",
    re.IGNORECASE,
)

# d <miesiąc> yyyy [HH:MM[:SS]]
RX_WORDS = re.compile(
    r"\b(?P<d>\d{1,2})\s+(?P<mname>[A-Za-ząćęłńóśźż]+)\s+(?P<y>\d{4})"
    r"(?:[ ,]*(?:o\s+)?"                        # separator / "o "
    r"(?P<h>\d{1,2}):(?P<min>\d{2})(?::(?P<s>\d{2}))?)?\b",
    re.IGNORECASE,
)

@dataclass(frozen=True)
class PolishHardFormatter:
    """Parsuje polskie formaty (numeryczny i słowny) z *opcjonalnym* czasem."""
    name: str = "pl-hard"

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = unicodedata.normalize("NFKC", text).strip()

        m = RX_NUMERIC.search(s)
        if m:
            d, mo, y = int(m["d"]), int(m["m"]), int(m["y"])
            h = int(m["h"]) if m["h"] else 0
            mi = int(m["min"]) if m["min"] else 0
            se = int(m["s"]) if m["s"] else 0
            try:
                return datetime(y, mo, d, h, mi, se)  # NAIVE – polityka nada TZ
            except ValueError:
                return None

        m = RX_WORDS.search(s.lower())
        if m:
            d, y = int(m["d"]), int(m["y"])
            mname = m["mname"]
            mo = PL_MONTHS.get(mname)
            if not mo:
                return None
            h = int(m["h"]) if m["h"] else 0
            mi = int(m["min"]) if m["min"] else 0
            se = int(m["s"]) if m["s"] else 0
            try:
                return datetime(y, mo, d, h, mi, se)  # NAIVE
            except ValueError:
                return None

        return None
