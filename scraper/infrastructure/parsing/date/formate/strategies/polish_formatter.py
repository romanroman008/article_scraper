# infrastructure/parsing/date/formatters/polish_hard_formatter.py
from __future__ import annotations

import logging
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

@dataclass(frozen=True, slots=True)
class PolishHardFormatter:
    name: str = "pl-hard"

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            self.log.debug("Pominięto formatowanie PL: pusty tekst wejściowy.")
            return None

        s = unicodedata.normalize("NFKC", str(text)).strip()

        # wariant numeryczny
        try:
            m = RX_NUMERIC.search(s)
        except Exception:
            self.log.error("Błąd regex dla formatu numerycznego PL.", exc_info=True)
            return None

        if m:
            try:
                d, mo, y = int(m["d"]), int(m["m"]), int(m["y"])
                h = int(m["h"]) if m["h"] else 0
                mi = int(m["min"]) if m["min"] else 0
                se = int(m["s"]) if m["s"] else 0
                dt = datetime(y, mo, d, h, mi, se)
                self.log.info('Sparsowano datę w formacie PL (numeryczny, iso="%s").', dt.isoformat())
                return dt
            except Exception:
                self.log.debug('Nieprawidłowa data w formacie numerycznym PL (próbka="%s").', s[:60])
                # próbujemy dalej wariant słowny

        # wariant słowny
        m = RX_WORDS.search(s.lower())
        if m:
            mname = m["mname"]
            mo = PL_MONTHS.get(mname)
            if not mo:
                self.log.debug('Nieznana nazwa miesiąca w formacie słownym PL (miesiąc="%s").', mname)
                return None
            try:
                d, y = int(m["d"]), int(m["y"])
                h = int(m["h"]) if m["h"] else 0
                mi = int(m["min"]) if m["min"] else 0
                se = int(m["s"]) if m["s"] else 0
                dt = datetime(y, mo, d, h, mi, se)
                self.log.info('Sparsowano datę w formacie PL (słowny, iso="%s").', dt.isoformat())
                return dt
            except Exception:
                self.log.debug('Nieprawidłowa data w formacie słownym PL (próbka="%s").', s[:60])
                return None

        self.log.debug("Nie rozpoznano daty w formacie PL (numeryczny ani słowny).")
        return None
