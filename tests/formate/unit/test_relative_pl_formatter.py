import pytest
from freezegun import freeze_time
import pytz
from datetime import datetime

from scraper.infrastructure.parsing.date.formate.strategies.relative_pl_formatter import RelativePlFormatter
from scraper.infrastructure.parsing.date.formate.utils import _aware  # jeśli używasz utils

TZ = pytz.timezone("Europe/Warsaw")

def _fmt(dt: datetime) -> str:
    return _aware(dt).strftime("%d.%m.%Y %H:%M:%S")

@freeze_time("2025-10-17 16:30:00", tz_offset=2)  # CEST dla Warszawy
def test_pl_yesterday_at():
    f = RelativePlFormatter()
    assert _fmt(f.format("Wczoraj o 13:00")) == "16.10.2025 13:00:00"

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("Dzisiaj", "17.10.2025 00:00:00"),
    ("Dziś",    "17.10.2025 00:00:00"),
    ("Wczoraj", "16.10.2025 00:00:00"),
    ("przed chwilą", "17.10.2025 16:30:00"),
])
def test_pl_keywords(text, expected):
    f = RelativePlFormatter()
    assert _fmt(f.format(text)) == expected

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("3h",             "17.10.2025 13:30:00"),
    ("15 min",         "17.10.2025 16:15:00"),
    ("10 sekund temu", "17.10.2025 16:29:50"),
    ("2 dni temu",     "15.10.2025 16:30:00"),
    ("1 tydzień temu", "10.10.2025 16:30:00"),
    ("3 miesiące temu","19.07.2025 16:30:00"),  # heurystyka 30 dni/miesiąc
    ("5 lat temu",     "18.10.2020 16:30:00"),  # heurystyka 365 dni/rok
])
def test_pl_units(text, expected):
    f = RelativePlFormatter()
    assert _fmt(f.format(text)) == expected

@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("Dziś wieczorem",      "17.10.2025 19:00:00"),
    ("Dzisiaj wcześniej",   "17.10.2025 12:00:00"),
    ("Wczoraj w nocy",      "16.10.2025 23:00:00"),
    ("Dziś rano",           "17.10.2025 09:00:00"),
    ("Dziś po południu",    "17.10.2025 15:00:00"),
    ("Dziś o 9.30",         "17.10.2025 09:30:00"),
])
def test_pl_compounds(text, expected):
    f = RelativePlFormatter()
    assert _fmt(f.format(text)) == expected
