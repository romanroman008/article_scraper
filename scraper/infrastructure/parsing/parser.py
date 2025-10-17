# scraper/infra/parser.py
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.extractor_chain import DateExtractorChain
from scraper.infrastructure.parsing.date.formate.formate_chain import DateFormatterChain
from scraper.infrastructure.parsing.date.formate.policy import ToUTCPolicy
from scraper.infrastructure.parsing.date.formate.strategies.iso8601z_formatter import ISO8601ZFormatter
from scraper.infrastructure.parsing.date.formate.strategies.polish_formatter import PolishHardFormatter

from scraper.infrastructure.parsing.date.extract.strategies.class_based_extractor import ClassBasedDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.meta_extractor import MetaDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.regex_fallback_extractor import RegexFallbackDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.time_tag_extractor import TimeTagDateExtractor
from scraper.infrastructure.parsing.date.parser_chain import extract_date_from_soup
from scraper.infrastructure.parsing.date.strategies.polish_patterns import SmartFormatter
from scraper.infrastructure.parsing.parsing_utils import pick_title, pick_container, html_to_text

from scraper.domain.models import ArticleData



class BeautifulSoupArticleParser:
    def parse(self, url: str, html: str) -> ArticleData:
        soup = BeautifulSoup(html, "html.parser")
        parser_chain = build_default_date_parser_chain()

        title = pick_title(soup)
        container = pick_container(soup)
        content_html = str(container) if container else html
        content_text = html_to_text(content_html)

        date = extract_date_from_soup(soup)
        # -> str | None
        raw_date = parser_chain.extract(soup)

        formatter = build_datetime_formatter_chain()

        new = formatter.try_format(raw_date)





        return ArticleData(
            url=url,
            title=title,
            content_html=content_html,
            content_text=content_text,
            published_at=date,
            source_domain=urlparse(url).netloc,
            raw_date= raw_date,
            new="DUPA",
        )





def build_default_date_parser_chain() -> DateExtractorChain:
    return DateExtractorChain(parsers=(
        MetaDateExtractor(),
        TimeTagDateExtractor(),
        ClassBasedDateExtractor(),
        RegexFallbackDateExtractor(),
    ))

def build_datetime_formatter_chain() -> DateFormatterChain:
    return DateFormatterChain(
        formatters=(
            ISO8601ZFormatter(),
            SmartFormatter(),
            PolishHardFormatter(),

        ),
        policy=ToUTCPolicy("Europe/Warsaw"),
    )