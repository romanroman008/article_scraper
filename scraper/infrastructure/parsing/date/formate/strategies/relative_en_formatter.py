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

@dataclass(frozen=True)
class RelativeEnFormatter:
    name: str = "relative-en"

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = text.strip().lower()

        # KLUCZOWE: bierz "teraz" z UTC, aby freezegun(tz_offset=...) nie dodawał +h
        now = datetime.utcnow()  # NAIVE, bez offsetu z freezegun

        # Złożone: yesterday/today at HH[:MM[:SS]]  → budujemy AWARE (Europe/Warsaw)
        if RX_EN_YESTERDAY_AT.search(s):
            t = _parse_time_at(s) or time(0, 0)
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, t.hour, t.minute, t.second))

        if RX_EN_TODAY_AT.search(s):
            t = _parse_time_at(s) or time(0, 0)
            return _aware(datetime(now.year, now.month, now.day, t.hour, t.minute, t.second))

        # Frazy słowne (AWARE)
        if RX_EN_THIS_MORNING.search(s):
            return _aware(datetime(now.year, now.month, now.day, MORNING.hour, MORNING.minute, 0))
        if RX_EN_THIS_AFTERNOON.search(s):
            return _aware(datetime(now.year, now.month, now.day, AFTERNOON.hour, AFTERNOON.minute, 0))
        if RX_EN_THIS_EVENING.search(s):
            return _aware(datetime(now.year, now.month, now.day, EVENING.hour, EVENING.minute, 0))
        if RX_EN_LAST_NIGHT.search(s):
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, LAST_NIGHT_TIME.hour, LAST_NIGHT_TIME.minute, 0))
        if RX_EN_EARLIER_TODAY.search(s):
            return _aware(datetime(now.year, now.month, now.day, EARLIER_TODAY.hour, EARLIER_TODAY.minute, 0))

        # Wczoraj / Dziś (AWARE)
        if RX_EN_YESTERDAY.search(s):
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, 0, 0, 0))
        if RX_EN_TODAY.search(s):
            return _aware(datetime(now.year, now.month, now.day, 0, 0, 0))

        # „just now”, „a moment ago” — NAIVE UTC "now" (testowe _fmt zrobi lokalizację)
        if RX_EN_JUST_NOW.search(s):
            return now

        # Jednostki względne — NAIVE (odliczane od utcnow)
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
                kwargs = {unit: n * mul}
                return now - timedelta(**kwargs)

        return None
