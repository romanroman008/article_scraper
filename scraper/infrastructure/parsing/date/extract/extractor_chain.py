from dataclasses import dataclass
from typing import Optional, Sequence

from bs4 import BeautifulSoup

from scraper.domain.ports import DateExtractor


@dataclass
class DateExtractorChain:
    parsers: Sequence[DateExtractor]

    def extract(self, soup: BeautifulSoup) -> Optional[str]:
        for p in self.parsers:
            result = p.extract(soup)
            if result:
                return result
        return None
