# infrastructure/parsing/date/formatters/iso8601z_formatter.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re

# Szybki filtr, żeby nie brać wszystkiego jak leci
ISO_RX = re.compile(
    r"^\s*\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
    r"(?:[.,]\d+)?"
    r"(?:Z|[+\-]\d{2}:\d{2})\s*$"
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
        # Normalizacje: 'Z' -> '+00:00', przecinek -> kropka, spacja -> 'T'
        s = s.replace("z", "Z")
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        # zamień pierwszy separator daty/czasu na 'T' (opcjonalne)
        if " " in s and "T" not in s[:20]:
            s = s.replace(" ", "T", 1)
        s = s.replace(",", ".")
        try:
            return datetime.fromisoformat(s)  # zwróci aware dt, jeśli był offset
        except ValueError:
            return None
