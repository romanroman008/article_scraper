# tests/formate/test_formatter_chain.py
import pytest
from freezegun import freeze_time

from scraper.infrastructure.parsing.date.formate.formate_chain import DateTimeFormatterChain
from scraper.infrastructure.parsing.date.formate.strategies.iso8601z_formatter import ISO8601ZFormatter
from scraper.infrastructure.parsing.date.formate.strategies.polish_formatter import PolishHardFormatter
from scraper.infrastructure.parsing.date.formate.strategies.relative_en_formatter import RelativeEnFormatter
from scraper.infrastructure.parsing.date.formate.strategies.relative_pl_formatter import RelativePlFormatter
from scraper.infrastructure.parsing.date.formate.strategies.smart_formatter import SmartFormatter


@freeze_time("2025-10-17 16:30:00", tz_offset=2)
@pytest.mark.parametrize("text,expected", [
    ("today at 9",        "17.10.2025 09:00:00"),
    ("this evening",      "17.10.2025 19:00:00"),
    ("wczoraj",           "16.10.2025 00:00:00"),
    ("dzisiaj o 15:45",   "17.10.2025 15:45:00"),
    ("przed chwilą",      "17.10.2025 16:30:00"),
    ("3h",                "17.10.2025 13:30:00"),
    ("2 tygodnie temu",   "03.10.2025 16:30:00"),
])


def test_chain_with_real_formatters(text, expected):
    chain = DateTimeFormatterChain([
            ISO8601ZFormatter(),
            RelativePlFormatter(),
            RelativeEnFormatter(),
            SmartFormatter(),
            PolishHardFormatter(),])
    assert chain.format(text).strftime("%d.%m.%Y %H:%M:%S") == expected
