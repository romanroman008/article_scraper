import logging
from dataclasses import dataclass
from datetime import timedelta, datetime, time
from typing import Optional

from scraper.infrastructure.parsing.date.const import TZ
from scraper.infrastructure.parsing.date.formate.utils import (
    RX_EN_JUST_NOW, RX_EN_SECONDS, RX_EN_MINUTES, RX_EN_HOURS,
    RX_EN_DAYS, RX_EN_WEEKS, RX_EN_MONTHS, RX_EN_YEARS,
    RX_EN_TODAY, RX_EN_YESTERDAY, RX_EN_EARLIER_TODAY,
    _aware, RX_EN_LAST_NIGHT, RX_EN_THIS_EVENING,
    RX_EN_THIS_AFTERNOON, RX_EN_THIS_MORNING,
    RX_EN_TODAY_AT, RX_EN_YESTERDAY_AT,
    _parse_time_at, MORNING, AFTERNOON, EVENING,
    LAST_NIGHT_TIME, EARLIER_TODAY
)

from dataclasses import dataclass
from datetime import timedelta, datetime, time
from typing import Optional

from scraper.infrastructure.parsing.date.const import TZ
from scraper.infrastructure.parsing.date.formate.utils import (
    RX_EN_JUST_NOW, RX_EN_SECONDS, RX_EN_MINUTES, RX_EN_HOURS,
    RX_EN_DAYS, RX_EN_WEEKS, RX_EN_MONTHS, RX_EN_YEARS,
    RX_EN_TODAY, RX_EN_YESTERDAY, RX_EN_EARLIER_TODAY,
    _aware, RX_EN_LAST_NIGHT, RX_EN_THIS_EVENING,
    RX_EN_THIS_AFTERNOON, RX_EN_THIS_MORNING,
    RX_EN_TODAY_AT, RX_EN_YESTERDAY_AT,
    _parse_time_at, MORNING, AFTERNOON, EVENING,
    LAST_NIGHT_TIME, EARLIER_TODAY
)

@dataclass(frozen=True, slots=True)
class RelativeEnFormatter:
    name: str = "relative-en"

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            self.log.debug("Pominięto formatowanie EN relative: pusty tekst wejściowy.")
            return None

        try:
            s = text.strip().lower()
            now = datetime.utcnow()  # NAIVE

            # yesterday/today at HH:MM[:SS]
            if RX_EN_YESTERDAY_AT.search(s):
                t = _parse_time_at(s) or time(0, 0)
                base = now - timedelta(days=1)
                dt = _aware(datetime(base.year, base.month, base.day, t.hour, t.minute, t.second))
                self.log.info('Rozpoznano frazę relatywną EN "yesterday at ..." (iso="%s").', dt.isoformat())
                return dt

            if RX_EN_TODAY_AT.search(s):
                t = _parse_time_at(s) or time(0, 0)
                dt = _aware(datetime(now.year, now.month, now.day, t.hour, t.minute, t.second))
                self.log.info('Rozpoznano frazę relatywną EN "today at ..." (iso="%s").', dt.isoformat())
                return dt

            # słowne
            if RX_EN_THIS_MORNING.search(s):
                dt = _aware(datetime(now.year, now.month, now.day, MORNING.hour, MORNING.minute, 0))
                self.log.info('Rozpoznano frazę EN "this morning" (iso="%s").', dt.isoformat())
                return dt
            if RX_EN_THIS_AFTERNOON.search(s):
                dt = _aware(datetime(now.year, now.month, now.day, AFTERNOON.hour, AFTERNOON.minute, 0))
                self.log.info('Rozpoznano frazę EN "this afternoon" (iso="%s").', dt.isoformat())
                return dt
            if RX_EN_THIS_EVENING.search(s):
                dt = _aware(datetime(now.year, now.month, now.day, EVENING.hour, EVENING.minute, 0))
                self.log.info('Rozpoznano frazę EN "this evening" (iso="%s").', dt.isoformat())
                return dt
            if RX_EN_LAST_NIGHT.search(s):
                base = now - timedelta(days=1)
                dt = _aware(datetime(base.year, base.month, base.day, LAST_NIGHT_TIME.hour, LAST_NIGHT_TIME.minute, 0))
                self.log.info('Rozpoznano frazę EN "last night" (iso="%s").', dt.isoformat())
                return dt
            if RX_EN_EARLIER_TODAY.search(s):
                dt = _aware(datetime(now.year, now.month, now.day, EARLIER_TODAY.hour, EARLIER_TODAY.minute, 0))
                self.log.info('Rozpoznano frazę EN "earlier today" (iso="%s").', dt.isoformat())
                return dt

            # yesterday/today bez czasu
            if RX_EN_YESTERDAY.search(s):
                base = now - timedelta(days=1)
                dt = _aware(datetime(base.year, base.month, base.day, 0, 0, 0))
                self.log.info('Rozpoznano frazę EN "yesterday" (iso="%s").', dt.isoformat())
                return dt
            if RX_EN_TODAY.search(s):
                dt = _aware(datetime(now.year, now.month, now.day, 0, 0, 0))
                self.log.info('Rozpoznano frazę EN "today" (iso="%s").', dt.isoformat())
                return dt

            # just now
            if RX_EN_JUST_NOW.search(s):
                self.log.info('Rozpoznano frazę EN "just now" (zwrócono utcnow).')
                return now

            # jednostki względne
            for rx, (unit, mul) in (
                (RX_EN_SECONDS, ("seconds", 1)),
                (RX_EN_MINUTES, ("minutes", 1)),
                (RX_EN_HOURS,   ("hours",   1)),
                (RX_EN_DAYS,    ("days",    1)),
                (RX_EN_WEEKS,   ("days",    7)),
                (RX_EN_MONTHS,  ("days",    30)),
                (RX_EN_YEARS,   ("days",    365)),
            ):
                m = rx.search(s)
                if m:
                    n = int(m.group(1))
                    dt = now - timedelta(**{unit: n * mul})
                    self.log.info('Rozpoznano frazę EN "%d %s ago" (zwrócono utcnow-%d%s).', n, unit, n*mul, unit)
                    return dt

            self.log.debug("Nie rozpoznano frazy relatywnej EN w podanym tekście.")
            return None

        except Exception:
            self.log.error("Błąd podczas formatowania relatywnego EN.", exc_info=True)
            return None