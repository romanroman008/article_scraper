
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional, Generator, Tuple, Sequence

from bs4 import BeautifulSoup

from scraper.domain.ports import DateParserText, DateExtractor
from scraper.infrastructure.parsing.const import TZ, DATE_META_SELECTORS
from scraper.infrastructure.parsing.date.strategies.polish_parser import PolishParser, RX_DDMMYYYY, RX_PL_WORDS

from scraper.infrastructure.parsing.date.strategies.smart_parser import SmartParser





def _format_output(dt: datetime) -> str:
    """dd.mm.yyyy HH:mm:ss w Europe/Warsaw; brak czasu => 00:00:00."""
    if dt.tzinfo is None:
        dt = TZ.localize(dt)
    else:
        dt = dt.astimezone(TZ)
    if dt.time() == time(0, 0):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt.strftime("%d.%m.%Y %H:%M:%S")


@dataclass
class ParserChain:
    parsers: tuple[DateParserText, ...] = (SmartParser(), PolishParser())

    def try_parse(self, text: str) -> Optional[str]:
        for p in self.parsers:
            dt = p.parse(text)
            if dt:
                return _format_output(dt)
        return None



def _iter_date_candidates(soup: BeautifulSoup) -> Generator[str, None, None]:
    # a) meta[content]
    for tag, attrs in DATE_META_SELECTORS:
        el = soup.find(tag, attrs)
        if el:
            content = (el.get("content") or "").strip()
            if content:
                yield content

    # b) <time> – atrybut datetime lub tekst
    for t in soup.find_all("time"):
        raw = (t.get("datetime") or t.get_text(" ", strip=True) or "").strip()
        if raw:
            yield raw

    # c) typowe klasy/sekcje z datą
    for el in soup.select('[class*="date"], [class*="time"], .post-meta, .entry-meta'):
        raw = el.get_text(" ", strip=True)
        if raw:
            yield raw

    # d) ostatnia deska ratunku – regexy PL na całym tekście
    text = (soup.get_text(" ", strip=True) or "").lower()
    for rx in (RX_DDMMYYYY, RX_PL_WORDS):
        m = rx.search(text)
        if m:
            yield m.group(0)


# --- API publiczne ------------------------------------------------------------

def extract_date_from_soup(soup: BeautifulSoup, chain: ParserChain | None = None) -> Optional[str]:
    """Zwraca datę publikacji w formacie 'dd.mm.yyyy HH:mm:ss' lub None."""
    chain = chain or ParserChain()
    for candidate in _iter_date_candidates(soup):
        result = chain.try_parse(candidate)
        if result:
            return result
    return None
