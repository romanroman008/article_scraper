from dataclasses import dataclass

@dataclass(frozen=True)
class ScraperDefaults:
    timezone: str = "Europe/Warsaw"
    languages: tuple[str, ...] = ("pl",)
    prefer_dates_from: str = "past"
    date_meta_selectors: tuple[tuple[str, dict[str, str]], ...] = (
        ("meta", {"property": "article:published_time"}),
        ("meta", {"name": "article:published_time"}),
        ("meta", {"property": "og:published_time"}),
        ("meta", {"itemprop": "datePublished"}),
        ("meta", {"name": "pubdate"}),
    )

DEFAULTS = ScraperDefaults()
