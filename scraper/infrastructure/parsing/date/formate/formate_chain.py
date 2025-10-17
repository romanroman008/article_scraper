# application/formatter_chain.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
from datetime import datetime

from scraper.domain.ports import DateFormatter
from scraper.infrastructure.parsing.date.formate.policy import ToUTCPolicy


@dataclass
class DateFormatterChain:
    formatters: Sequence[DateFormatter]
    policy: ToUTCPolicy

    def try_format(self, text: str) -> Optional[datetime]:
        if not text:
            return None
        for f in self.formatters:
            dt = f.format(text)
            if dt is not None:
                return self.policy.apply(dt)
        return None
