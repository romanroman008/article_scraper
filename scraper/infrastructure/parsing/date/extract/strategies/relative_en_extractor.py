# scraper/infrastructure/parsing/date/extract/strategies/relative_en_extractor.py
from __future__ import annotations
import re
from typing import Optional
from bs4 import BeautifulSoup

REL_WITH_TIME_EN = re.compile(
    r"""(?ixu)\b
    (?:
        (?:yesterday|today)\s+(?:at)\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?
    )\b"""
)

REL_COMPOUNDS_EN = re.compile(
    r"""(?ixu)\b(?:
        earlier\ today |
        this\ (?:morning|afternoon|evening) |
        last\ night
    )\b"""
)

SECONDS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<sec>\d+)\s*(?:s|sec|secs|second|seconds)\s*(?:ago)\b"""
)
SECONDS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<sec>\d+)\s*(?:s|sec|secs|second|seconds)\b"""
)

MINUTES_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<min>\d+)\s*(?:m|min|mins|minute|minutes)\s*(?:ago)\b"""
)
MINUTES_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<min>\d+)\s*(?:m|min|mins|minute|minutes)\b"""
)

HOURS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<h>\d+)\s*(?:h|hr|hrs|hour|hours)\s*(?:ago)\b"""
)
HOURS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<h>\d+)\s*(?:h|hr|hrs|hour|hours)\b"""
)

DAYS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<d>\d+)\s*(?:d|day|days)\s*(?:ago)\b|\bsprzed-non-en-never\b"""  # sentinel
)
DAYS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<d>\d+)\s*(?:d|day|days)\b"""
)

WEEKS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<w>\d+)\s*(?:wk|wks|week|weeks)\s*(?:ago)\b"""
)
WEEKS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<w>\d+)\s*(?:wk|wks|week|weeks)\b"""
)

MONTHS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<mo>\d+)\s*(?:month|months)\s*(?:ago)\b"""
)
MONTHS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<mo>\d+)\s*(?:month|months)\b"""
)

YEARS_WITH_SUFFIX_EN = re.compile(
    r"""(?ixu)\b(?P<y>\d+)\s*(?:yr|yrs|year|years)\s*(?:ago)\b"""
)
YEARS_BARE_EN = re.compile(
    r"""(?ixu)\b(?P<y>\d+)\s*(?:yr|yrs|year|years)\b"""
)

KEYWORDS_EN = re.compile(r"""(?ixu)\b(yesterday|today)\b""")
JUST_NOW_EN = re.compile(r"""(?ixu)\b(just\ now|a\ moment\ ago|moments?\ ago)\b""")

class RelativeEnTextDateExtractor:
    name = "relative-text-en"
    _CONTAINER_SELECTOR = (
        "header, time, .post-meta, .entry-meta, [class*='date'], [class*='time'], "
        "meta[name*='date'], meta[property*='date']"
    )
    _PATTERNS = [
        REL_WITH_TIME_EN,
        REL_COMPOUNDS_EN,
        SECONDS_WITH_SUFFIX_EN, MINUTES_WITH_SUFFIX_EN, HOURS_WITH_SUFFIX_EN,
        DAYS_WITH_SUFFIX_EN, WEEKS_WITH_SUFFIX_EN, MONTHS_WITH_SUFFIX_EN, YEARS_WITH_SUFFIX_EN,
        SECONDS_BARE_EN, MINUTES_BARE_EN, HOURS_BARE_EN,
        DAYS_BARE_EN, WEEKS_BARE_EN, MONTHS_BARE_EN, YEARS_BARE_EN,
        JUST_NOW_EN, KEYWORDS_EN,
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
