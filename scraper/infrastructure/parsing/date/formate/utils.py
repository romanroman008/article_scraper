import re
from datetime import time, datetime
from typing import Optional

from scraper.infrastructure.parsing.date.const import TZ

_TIME_AT_RE = re.compile(r"(?ixu)\b(?:at|o)\s+(\d{1,2})(?::(\d{2}))?(?::(\d{2}))?(?:[.,](\d{1,2}))?\b")

def _parse_time_at(text: str) -> Optional[time]:
    m = _TIME_AT_RE.search(text)
    if not m:
        return None
    h = int(m.group(1))
    mi = int(m.group(2) or m.group(4) or 0)
    s = int(m.group(3) or 0)
    if 0 <= h <= 23 and 0 <= mi <= 59 and 0 <= s <= 59:
        return time(h, mi, s)
    return None

def _aware(dt: datetime) -> datetime:
    """Upewnij się, że datetime ma TZ (Europe/Warsaw)."""
    if TZ is None:
        return dt  # fallback – pozostaw NAIVE, Twój format_to_string... i tak zlokalizuje
    if dt.tzinfo is None:
        return TZ.localize(dt)
    return dt

# Heurystyki dla fraz */
MORNING   = time(9, 0)
AFTERNOON = time(15, 0)
EVENING   = time(19, 0)
LAST_NIGHT_TIME = time(23, 0)
EARLIER_TODAY  = time(12, 0)

# =========================
# EN formatter
# =========================

# Słowa kluczowe / kompozyty
RX_EN_YESTERDAY_AT = re.compile(r"(?ixu)\byesterday\s+at\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?\b")
RX_EN_TODAY_AT     = re.compile(r"(?ixu)\btoday\s+at\s+\d{1,2}(?::\d{2})?(?::\d{2})?(?:[.,]\d{1,2})?\b")
RX_EN_THIS_MORNING = re.compile(r"(?ixu)\bthis\s+morning\b")
RX_EN_THIS_AFTERNOON = re.compile(r"(?ixu)\bthis\s+afternoon\b")
RX_EN_THIS_EVENING = re.compile(r"(?ixu)\bthis\s+evening\b")
RX_EN_LAST_NIGHT   = re.compile(r"(?ixu)\blast\s+night\b")
RX_EN_EARLIER_TODAY= re.compile(r"(?ixu)\bearlier\s+today\b")
RX_EN_YESTERDAY    = re.compile(r"(?ixu)\byesterday\b")
RX_EN_TODAY        = re.compile(r"(?ixu)\btoday\b")
RX_EN_JUST_NOW     = re.compile(r"(?ixu)\b(?:just\s+now|a\s+moment\s+ago|moments?\s+ago)\b")

# Jednostki względne (z „ago” lub nagie skróty)
RX_EN_SECONDS = re.compile(r"(?ixu)\b(\d+)\s*(?:s|sec|secs|second|seconds)(?:\s*ago)?\b")
RX_EN_MINUTES = re.compile(r"(?ixu)\b(\d+)\s*(?:m|min|mins|minute|minutes)(?:\s*ago)?\b")
RX_EN_HOURS   = re.compile(r"(?ixu)\b(\d+)\s*(?:h|hr|hrs|hour|hours)(?:\s*ago)?\b")
RX_EN_DAYS    = re.compile(r"(?ixu)\b(\d+)\s*(?:d|day|days)(?:\s*ago)?\b")
RX_EN_WEEKS   = re.compile(r"(?ixu)\b(\d+)\s*(?:wk|wks|week|weeks)(?:\s*ago)?\b")
RX_EN_MONTHS  = re.compile(r"(?ixu)\b(\d+)\s*(?:month|months)(?:\s*ago)?\b")
RX_EN_YEARS   = re.compile(r"(?ixu)\b(\d+)\s*(?:yr|yrs|year|years)(?:\s*ago)?\b")




