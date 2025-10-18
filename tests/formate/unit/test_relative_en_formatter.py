import pytest
from freezegun import freeze_time
from datetime import datetime
import pytz

from scraper.infrastructure.parsing.date.formate.strategies.relative_en_formatter import RelativeEnFormatter
from scraper.infrastructure.parsing.date.formate.utils import _aware

TZ = pytz.timezone("Europe/Warsaw")

def _fmt(dt: datetime) -> str:
    return _aware(dt).strftime("%d.%m.%Y %H:%M:%S")

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
def test_en_today_at():
    f = RelativeEnFormatter()
    assert _fmt(f.format("today at 9")) == "17.10.2025 09:00:00"

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("yesterday",      "16.10.2025 00:00:00"),
    ("today",          "17.10.2025 00:00:00"),
    ("just now",       "17.10.2025 16:30:00"),
    ("a moment ago",   "17.10.2025 16:30:00"),
])
def test_en_keywords(text, expected):
    f = RelativeEnFormatter()
    assert _fmt(f.format(text)) == expected

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("3h",            "17.10.2025 13:30:00"),
    ("15 minutes ago","17.10.2025 16:15:00"),
    ("45s ago",       "17.10.2025 16:29:15"),
    ("3 days ago",    "14.10.2025 16:30:00"),
    ("2 weeks ago",   "03.10.2025 16:30:00"),
    ("1 month ago",   "17.09.2025 16:30:00"),  # 30 dni
    ("2 years ago",   "18.10.2023 16:30:00"),  # 365 dni/rok
])
def test_en_units(text, expected):
    f = RelativeEnFormatter()
    assert _fmt(f.format(text)) == expected

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("this morning",   "17.10.2025 09:00:00"),
    ("this afternoon", "17.10.2025 15:00:00"),
    ("this evening",   "17.10.2025 19:00:00"),
    ("last night",     "16.10.2025 23:00:00"),
    ("yesterday at 23:59:59", "16.10.2025 23:59:59"),
])
def test_en_compounds(text, expected):
    f = RelativeEnFormatter()
    assert _fmt(f.format(text)) == expected
