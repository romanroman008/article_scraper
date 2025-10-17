from django.conf import settings
from .conf import DEFAULTS, ScraperDefaults

def get_scraper_settings() -> ScraperDefaults:
    cfg = getattr(settings, "SCRAPER", {})
    return ScraperDefaults(
        timezone = cfg.get("TIMEZONE", getattr(settings, "TIME_ZONE", DEFAULTS.timezone)),
        languages = tuple(cfg.get("LANGUAGES", DEFAULTS.languages)),
        prefer_dates_from = cfg.get("PREFER_DATES_FROM", DEFAULTS.prefer_dates_from),
        date_meta_selectors = tuple(cfg.get("DATE_META_SELECTORS", DEFAULTS.date_meta_selectors)),
    )
