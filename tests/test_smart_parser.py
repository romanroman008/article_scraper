from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from scraper.infrastructure.parsing.date.strategies.smart_parser import SmartParser


@pytest.fixture
def parser():
    return SmartParser()


def _is_warsaw_tz(dt: datetime) -> bool:
    """Lekka asercja: datetime jest timezone-aware i z offsetem właściwym dla PL (CET/CEST)."""
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    # CEST = +2h (lato), CET = +1h (zima) — zależnie od daty.
    return dt.utcoffset() in (timedelta(hours=1), timedelta(hours=2))


def test_returns_none_on_empty_or_none(parser):
    assert parser.parse("") is None
    assert parser.parse("   ") is None
    assert parser.parse(None) is None  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("2024-10-14", datetime(2024, 10, 14, 0, 0)),                    # ISO bez czasu
        ("14.10.2024", datetime(2024, 10, 14, 0, 0)),                    # PL dd.mm.yyyy
        ("14 października 2024", datetime(2024, 10, 14, 0, 0)),          # PL nazwa miesiąca
        ("2024-12-01 08:15:30+01:00", datetime(2024, 12, 1, 8, 15, 30)), # z offsetem zimowym (CET)
    ],
)
def test_parses_absolute_dates_pl_and_iso(parser, text, expected):
    dt = parser.parse(text)
    assert dt is not None
    # ta asercja toleruje konwersję do Europe/Warsaw (TO_TIMEZONE)
    assert dt.year == expected.year and dt.month == expected.month and dt.day == expected.day
    assert dt.hour == expected.hour and dt.minute == expected.minute and dt.second == expected.second
    assert _is_warsaw_tz(dt)


def test_parses_iso_z_and_converts_to_warsaw(parser):
    # 2024-10-14T18:45:00Z => w Warszawie (CEST, UTC+2) będzie 20:45
    dt = parser.parse("2024-10-14T18:45:00Z")
    assert dt is not None
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) == (2024, 10, 14, 20, 45, 0)
    assert _is_warsaw_tz(dt)


@freeze_time("2025-10-17 12:34:56+02:00")  # piątek, CEST w Warszawie
def test_relative_yesterday_keeps_time_component(parser):
    dt = parser.parse("wczoraj")
    # „wczoraj” powinno odjąć 1 dzień od RELATIVE_BASE
    assert dt is not None
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) == (2025, 10, 16, 12, 34, 56)
    assert _is_warsaw_tz(dt)


@freeze_time("2025-10-17 12:34:56+02:00")
def test_relative_two_days_ago(parser):
    dt = parser.parse("2 dni temu")
    assert dt is not None
    # odejmuje całe 2 dni, zachowując komponent czasu
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) == (2025, 10, 15, 12, 34, 56)
    assert _is_warsaw_tz(dt)


@freeze_time("2025-10-17 12:34:56+02:00")
def test_relative_three_hours_ago(parser):
    dt = parser.parse("3 godziny temu")
    assert dt is not None
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second) == (2025, 10, 17, 9, 34, 56)
    assert _is_warsaw_tz(dt)


@freeze_time("2025-10-17 12:34:56+02:00")
def test_ambiguous_without_year_prefers_past(parser):
    # PREFER_DATES_FROM = past => „1 marca” w październiku 2025 to 2025-03-01 (przeszłość)
    dt = parser.parse("1 marca")
    assert dt is not None
    assert (dt.year, dt.month, dt.day) == (2025, 3, 1)
    # brak godziny zwykle da 00:00:00 — ale to zachowanie dateparsera;
    # normalizacja do 00:00:00 jeśli brak czasu robimy wyżej (w agregatorze).
    assert _is_warsaw_tz(dt)


def test_trims_whitespace_and_parses(parser):
    dt = parser.parse("   14.10.2024   ")
    assert dt is not None
    assert (dt.year, dt.month, dt.day) == (2024, 10, 14)
    assert _is_warsaw_tz(dt)
