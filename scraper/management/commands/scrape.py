# scraper/management/commands/scrape.py
import logging

from django.core.management.base import BaseCommand

# zainicjuj renderer, jeśli chcesz fallback JS:
# from scraper.infra.renderer import PlaywrightRenderer
from scraper.app.use_cases import ScrapeArticlesUseCase
from scraper.infrastructure.parsing.parser import BeautifulSoupArticleParser
from scraper.infrastructure.playwright_renderer import PlaywrightRenderer
from scraper.infrastructure.repository import DjangoArticleRepository
from scraper.infrastructure.request_html_fetcher import RequestsHtmlFetcher

DEFAULT_URLS = [
    "https://galicjaexpress.pl/ford-c-max-jaki-silnik-benzynowy-wybrac-aby-zaoszczedzic-na-paliwie",
    "https://galicjaexpress.pl/bmw-e9-30-cs-szczegolowe-informacje-o-osiagach-i-historii-modelu",
    "https://take-group.github.io/example-blog-without-ssr/jak-kroic-piers-z-kurczaka-aby-uniknac-suchych-kawalkow-miesa",
    "https://take-group.github.io/example-blog-without-ssr/co-mozna-zrobic-ze-schabu-oprocz-kotletow-5-zaskakujacych-przepisow",
]

class Command(BaseCommand):
    help = "Scrape predefined articles and store them in DB"

    def add_arguments(self, parser):
        parser.add_argument("--url", action="append", help="Możesz podać wiele razy")

    def handle(self, *args, **opts):
        urls = opts.get("url") or DEFAULT_URLS
        total = len(urls)
        logging.info(f"Scraping {total} article(s)...")

        use_case = ScrapeArticlesUseCase(
            fetcher=RequestsHtmlFetcher(),
            parser=BeautifulSoupArticleParser(),
            repository=DjangoArticleRepository(),
            renderer=PlaywrightRenderer(),  # lub PlaywrightRenderer()
            min_text_len=150
        )
        stats = use_case.run(urls)
        logging.info(f"Done. Created: {stats['created']}, Skipped: {stats['skipped']}, Failed: {stats['failed']}, Total: {total}")
