from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass(frozen=True)
class SmartParser:
    """Ogólny parser oparty o dateparser (jęz. PL, tz=Europe/Warsaw)."""
    name: str = "smart"

    def parse(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        import dateparser  # lokalny import, by nie degradować cold startu

        # Język przekazujemy argumentem `languages`, NIE w `settings`
        dt = dateparser.parse(
            text.strip(),
            languages=["pl"],
            settings={
                "PREFER_DATES_FROM": "past",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "TIMEZONE": "Europe/Warsaw",
                "TO_TIMEZONE": "Europe/Warsaw",

            },
        )
        return dt