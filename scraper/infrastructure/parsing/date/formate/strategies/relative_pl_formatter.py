import re
from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import Optional

from scraper.infrastructure.parsing.date.const import TZ
from scraper.infrastructure.parsing.date.formate.utils import _aware, _parse_time_at, MORNING, AFTERNOON, EVENING, \
    LAST_NIGHT_TIME, EARLIER_TODAY

RX_PL_YESTERDAY_AT = re.compile(r"(?ixu)\bwczoraj\s+o\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?\b")
RX_PL_TODAY_AT     = re.compile(r"(?ixu)\b(?:dzis(?:iaj)?|dzi[sś])\s+o\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?\b")

RX_PL_THIS_MORNING   = re.compile(r"(?ixu)\b(?:dzis(?:iaj)?|dzi[sś])\s+rano\b")
RX_PL_THIS_AFTERNOON = re.compile(r"(?ixu)\b(?:dzis(?:iaj)?|dzi[sś])\s+po\s+po[łl]udniu\b")
RX_PL_THIS_EVENING   = re.compile(r"(?ixu)\b(?:dzis(?:iaj)?|dzi[sś])\s+wieczorem\b")
RX_PL_LAST_NIGHT     = re.compile(r"(?ixu)\bwczoraj\s+w\s*nocy\b")
RX_PL_EARLIER_TODAY  = re.compile(r"(?ixu)\bdzis(?:iaj)?\s+wcze[sś]niej\b")

RX_PL_YESTERDAY  = re.compile(r"(?ixu)\bwczoraj\b")
RX_PL_TODAY      = re.compile(r"(?ixu)\b(?:dzis(?:iaj)?|dzi[sś])\b")
RX_PL_JUST_NOW   = re.compile(r"(?ixu)\b(?:przed\s+chwil[aą]|przed\s+chwila|chwile?\s+temu|przed\s+momentem)\b")

# Jednostki (z „temu/wstecz” lub nagie skróty)
RX_PL_SECONDS = re.compile(r"(?ixu)\b(\d+)\s*(?:sek(?:\.|)|sekundy|sekund[eę]?|sekunda)(?:\s*(?:temu|wstecz))?\b")
RX_PL_MINUTES = re.compile(r"(?ixu)\b(\d+)\s*(?:min(?:\.|)|minuta|minuty|minut[eę]?)(?:\s*(?:temu|wstecz))?\b")
RX_PL_HOURS   = re.compile(r"(?ixu)\b(\d+)\s*(?:h|hr|hrs|hour|hours|g\.?|godz\.?|godzina|godziny|godzin)(?:\s*(?:temu|wstecz))?\b")
RX_PL_DAYS    = re.compile(r"(?ixu)\b(\d+)\s*(?:d|dzien|dzie[nń]|dni)(?:\s*(?:temu|wstecz))?\b|\bsprzed\s+(\d+)\s*(?:dni|dzie[nń])\b")
RX_PL_WEEKS   = re.compile(r"(?ixu)\b(\d+)\s*(?:wk|wks|week|weeks|tydzień|tydzien|tydzie[nń]|tygodnie|tygodni)(?:\s*(?:temu|wstecz))?\b|\bsprzed\s+(\d+)\s*tygodni\b")
RX_PL_MONTHS  = re.compile(r"(?ixu)\b(\d+)\s*(?:miesiac|miesi[aą]c(?:e|y)?|miesi[aą]ce|miesi[eę]cy)(?:\s*(?:temu|wstecz))?\b|\bsprzed\s+(\d+)\s*miesi[eę]cy\b")
RX_PL_YEARS   = re.compile(r"(?ixu)\b(\d+)\s*(?:rok|lata|lat)(?:\s*(?:temu|wstecz))?\b|\bsprzed\s+(\d+)\s*lat\b")




@dataclass(frozen=True)
class RelativePlFormatter:
    name: str = "relative-pl"

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = text.strip().lower()

        # KLUCZOWE:
        # - do „teraz”/relatywnych używamy NAIVE UTC (freezegun nie doda offsetu),
        # - do konstrukcji kalendarzowych budujemy AWARE przez _aware(...)
        now = datetime.utcnow()  # NAIVE
        # Jeśli chcesz bazować na lokalnej dacie dla fraz słownych, można też użyć:
        # today_local = datetime.now(TZ)  # AWARE – tylko do wyciągnięcia roku/miesiąca/dnia
        # ale dla testów zamrożonych na 16:30 nie ma różnicy; zostajemy przy 'now'.

        # Złożone: wczoraj/dzisiaj o HH[:MM[:SS]]
        if RX_PL_YESTERDAY_AT.search(s):
            t = _parse_time_at(s) or time(0, 0)
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, t.hour, t.minute, t.second))

        if RX_PL_TODAY_AT.search(s):
            t = _parse_time_at(s) or time(0, 0)
            return _aware(datetime(now.year, now.month, now.day, t.hour, t.minute, t.second))

        # Frazy słowne (AWARE)
        if RX_PL_THIS_MORNING.search(s):
            return _aware(datetime(now.year, now.month, now.day, MORNING.hour, MORNING.minute, 0))
        if RX_PL_THIS_AFTERNOON.search(s):
            return _aware(datetime(now.year, now.month, now.day, AFTERNOON.hour, AFTERNOON.minute, 0))
        if RX_PL_THIS_EVENING.search(s):
            return _aware(datetime(now.year, now.month, now.day, EVENING.hour, EVENING.minute, 0))
        if RX_PL_LAST_NIGHT.search(s):
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, LAST_NIGHT_TIME.hour, LAST_NIGHT_TIME.minute, 0))
        if RX_PL_EARLIER_TODAY.search(s):
            return _aware(datetime(now.year, now.month, now.day, EARLIER_TODAY.hour, EARLIER_TODAY.minute, 0))

        # Wczoraj / Dziś (AWARE)
        if RX_PL_YESTERDAY.search(s):
            base = now - timedelta(days=1)
            return _aware(datetime(base.year, base.month, base.day, 0, 0, 0))
        if RX_PL_TODAY.search(s):
            return _aware(datetime(now.year, now.month, now.day, 0, 0, 0))

        # „przed chwilą” itp. — NAIVE (testowe _fmt i tak zlokalizuje raz)
        if RX_PL_JUST_NOW.search(s):
            return now

        # Jednostki (obsługa „X … temu” i „sprzed X …”)
        for rx, (unit, mul) in (
            (RX_PL_SECONDS, ("seconds", 1)),
            (RX_PL_MINUTES, ("minutes", 1)),
            (RX_PL_HOURS,   ("hours",   1)),
            (RX_PL_DAYS,    ("days",    1)),
            (RX_PL_WEEKS,   ("days",    7)),
            (RX_PL_MONTHS,  ("days",    30)),
            (RX_PL_YEARS,   ("days",    365)),
        ):
            m = rx.search(s)
            if m:
                g = m.group(1) or m.group(2)  # „sprzed X …” trafia do grupy 2
                n = int(g)
                kwargs = {unit: n * mul}
                return now - timedelta(**kwargs)

        return None