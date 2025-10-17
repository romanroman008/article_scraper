from typing import Tuple

import pytz

TZ = pytz.timezone("Europe/Warsaw")

DATE_META_SELECTORS: list[Tuple[str, dict[str, str]]] = [
    ("meta", {"property": "article:published_time"}),
    ("meta", {"name": "article:published_time"}),
    ("meta", {"property": "og:published_time"}),
    ("meta", {"itemprop": "datePublished"}),
    ("meta", {"name": "pubdate"}),
]