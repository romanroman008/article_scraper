# application/datetime_normalization.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
import pytz

@dataclass(frozen=True)
class ToUTCPolicy:
    """Naive => załóż Europe/Warsaw; wynik zawsze w UTC."""
    tz_name: str = "Europe/Warsaw"

    def apply(self, dt: datetime) -> datetime:
        tz = pytz.timezone(self.tz_name)
        if dt.tzinfo is None:
            dt = tz.localize(dt)
        return dt.astimezone(timezone.utc)
