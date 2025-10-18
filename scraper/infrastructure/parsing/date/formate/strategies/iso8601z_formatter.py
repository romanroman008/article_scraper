# infrastructure/parsing/date/formatters/iso8601z_formatter.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

ISO_RX = re.compile(
    r"^\s*\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+\-]\d{2}:\d{2})\s*$"
)

@dataclass(frozen=True)
class ISO8601ZFormatter:
    name: str = "iso8601z"
    def format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        s = text.strip()
        if not ISO_RX.match(s):
            return None
        s = s.replace(",", ".")
        if s.endswith("Z") or s.endswith("z"):
            s = s[:-1] + "+00:00"
        if " " in s and "T" not in s[:20]:
            s = s.replace(" ", "T", 1)
        try:
            return datetime.fromisoformat(s)  # aware jeśli jest offset
        except ValueError:
            return None
