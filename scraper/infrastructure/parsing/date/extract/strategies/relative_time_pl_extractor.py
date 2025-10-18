# scraper/infrastructure/parsing/date/extract/strategies/relative_pl_extractor.py
from __future__ import annotations
import re
from typing import Optional
from bs4 import BeautifulSoup

REL_WITH_TIME_PL = re.compile(
    r"""(?ixu)\b
    (?:
        (?:wczoraj|dzis(?:iaj)?|dzi[sś])\s+(?:o)\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?
    )\b"""
)

REL_COMPOUNDS_PL = re.compile(
    r"""(?ixu)\b(?:
        dzis(?:iaj)?\s+wcze[sś]niej |
        (?:dzis(?:iaj)?|dzi[sś])\s+(?:rano|po\ s*po[łl]udniu|wieczorem) |
        wczoraj\ \s*(?:w\ s*nocy|wieczorem)
    )\b"""
)

SECONDS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<sec>\d+)\s*(?:sek(?:\.|)|sekundy|sekund[eę]?|sekunda)\s*(?:temu|wstecz)\b"""
)
SECONDS_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<sec>\d+)\s*(?:sek(?:\.|)|sekundy|sekund[eę]?|sekunda)\b"""
)

MINUTES_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<min>\d+)\s*(?:min(?:\.|)|minuta|minuty|minut[eę]?)\s*(?:temu|wstecz)\b"""
)
MINUTES_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<min>\d+)\s*(?:min(?:\.|)|minuta|minuty|minut[eę]?)\b"""
)

HOURS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b
    (?P<h>\d+)\s*
    (?:
        h|hr|hrs|hour|hours              
      | g\.?|godz\.?|godzina|godziny|godzin
    )
    \s*(?:temu|wstecz)
    \b"""
)

HOURS_BARE_PL = re.compile(
    r"""(?ixu)\b
    (?P<h>\d+)\s*
    (?:
        h|hr|hrs|hour|hours              
      | g\.?|godz\.?|godzina|godziny|godzin
    )
    \b"""
)

DAYS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<d>\d+)\s*(?:dzien|dzie[nń]|dni)\s*(?:temu|wstecz)\b|\bsprzed\s+(?P<d2>\d+)\s*(?:dni|dzie[nń])\b"""
)
DAYS_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<d>\d+)\s*(?:dzien|dzie[nń]|dni)\b"""
)

WEEKS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<w>\d+)\s*(?:tydzień|tydzien|tydzie[nń]|tygodnie|tygodni)\s*(?:temu|wstecz)\b|
        \bsprzed\s+(?P<w2>\d+)\s*(?:tygodni)\b"""
)
WEEKS_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<w>\d+)\s*(?:tydzień|tydzien|tydzie[nń]|tygodnie|tygodni)\b"""
)

MONTHS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<mo>\d+)\s*(?:miesiac|miesi[aą]c(?:e|y)?|miesi[aą]ce|miesi[eę]cy)\s*(?:temu|wstecz)\b|
        \bsprzed\s+(?P<mo2>\d+)\s*(?:miesi[eę]cy)\b"""
)
MONTHS_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<mo>\d+)\s*(?:miesiac|miesi[aą]c(?:e|y)?|miesi[aą]ce|miesi[eę]cy)\b"""
)

YEARS_WITH_SUFFIX_PL = re.compile(
    r"""(?ixu)\b(?P<y>\d+)\s*(?:rok|lata|lat)\s*(?:temu|wstecz)\b|\bsprzed\s+(?P<y2>\d+)\s*(?:lat)\b"""
)
YEARS_BARE_PL = re.compile(
    r"""(?ixu)\b(?P<y>\d+)\s*(?:rok|lata|lat)\b"""
)

KEYWORDS_PL = re.compile(r"""(?ixu)\b(wczoraj|dzis(?:iaj)?|dzi[sś])\b""")
JUST_NOW_PL = re.compile(r"""(?ixu)\b(przed\ chwil[aą]|przed\ chwila|chwile?\ temu|przed\ momentem)\b""")

class RelativePlTextDateExtractor:
    name = "relative-text-pl"
    _CONTAINER_SELECTOR = (
        "header, time, .post-meta, .entry-meta, [class*='date'], [class*='time'], "
        "meta[name*='date'], meta[property*='date']"
    )
    _PATTERNS = [
        REL_WITH_TIME_PL,
        REL_COMPOUNDS_PL,
        SECONDS_WITH_SUFFIX_PL, MINUTES_WITH_SUFFIX_PL, HOURS_WITH_SUFFIX_PL,
        DAYS_WITH_SUFFIX_PL, WEEKS_WITH_SUFFIX_PL, MONTHS_WITH_SUFFIX_PL, YEARS_WITH_SUFFIX_PL,
        SECONDS_BARE_PL, MINUTES_BARE_PL, HOURS_BARE_PL,
        DAYS_BARE_PL, WEEKS_BARE_PL, MONTHS_BARE_PL, YEARS_BARE_PL,
        JUST_NOW_PL, KEYWORDS_PL,
    ]

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        containers = soup.select(self._CONTAINER_SELECTOR) or [soup]
        for el in containers:
            text = (el.get_text(" ", strip=True) or "") if hasattr(el, "get_text") else ""
            if not text:
                continue
            lower = text.lower()
            for rx in self._PATTERNS:
                m = rx.search(lower)
                if m:
                    return m.group(0).strip()
        return None
