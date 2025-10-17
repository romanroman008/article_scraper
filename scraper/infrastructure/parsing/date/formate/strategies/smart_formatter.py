# infrastructure/parsing/date/formatters/smart_formatter.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class SmartFormatter:
    """Ogólny formater oparty o dateparser (PL, tz=Europe/Warsaw)."""
    name: str = "smart"

    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        # lokalny import – szybszy cold start
        import dateparser
        dt = dateparser.parse(
            text.strip(),
            languages=["pl"],
            settings={
                "PREFER_DATES_FROM": "past",
                "RETURN_AS_TIMEZONE_AWARE": True,  # -> aware
                "TIMEZONE": "Europe/Warsaw",
                "TO_TIMEZONE": "Europe/Warsaw",
            },
        )
        # dateparser potrafi zwrócić None
        return dt
