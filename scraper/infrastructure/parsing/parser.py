# scraper/infra/parser.py
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.extractor_chain import DateExtractorChain
from scraper.infrastructure.parsing.date.extract.strategies.relative_en_extractor import RelativeEnTextDateExtractor
from scraper.infrastructure.parsing.date.formate.formate_chain import DateTimeFormatterChain


from scraper.infrastructure.parsing.date.formate.strategies.iso8601z_formatter import ISO8601ZFormatter
from scraper.infrastructure.parsing.date.formate.strategies.polish_formatter import PolishHardFormatter

from scraper.infrastructure.parsing.date.extract.strategies.class_based_extractor import ClassBasedDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.meta_extractor import MetaDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.regex_fallback_extractor import RegexFallbackDateExtractor
from scraper.infrastructure.parsing.date.extract.strategies.time_tag_extractor import TimeTagDateExtractor
from scraper.infrastructure.parsing.date.formate.strategies.relative_en_formatter import RelativeEnFormatter
from scraper.infrastructure.parsing.date.formate.strategies.relative_pl_formatter import RelativePlFormatter
from scraper.infrastructure.parsing.date.formate.strategies.smart_formatter import SmartFormatter

from scraper.infrastructure.parsing.parsing_utils import pick_title, pick_container, html_to_text

from scraper.domain.models import ArticleData



class BeautifulSoupArticleParser:
    def parse(self, url: str, html: str) -> ArticleData:
        soup = BeautifulSoup(html, "html.parser")
        extractor_chain = build_default_date_extractor_chain()
        formatter_chain = build_datetime_formatter_chain()

        title = pick_title(soup)
        container = pick_container(soup)
        content_html = str(container) if container else html
        content_text = html_to_text(content_html)



        raw_date = extractor_chain.extract(soup)
        date = formatter_chain.format(raw_date)



        return ArticleData(
            url=url,
            title=title,
            content_html=content_html,
            content_text=content_text,
            published_at=date,
            source_domain=urlparse(url).netloc,
        )





def build_default_date_extractor_chain() -> DateExtractorChain:
    return DateExtractorChain(parsers=(
        MetaDateExtractor(),
        TimeTagDateExtractor(),
        RelativeEnTextDateExtractor(),
        RelativeEnTextDateExtractor(),
        ClassBasedDateExtractor(),
        RegexFallbackDateExtractor(),
    ))


def build_datetime_formatter_chain() -> DateTimeFormatterChain:
    return DateTimeFormatterChain(
        formatters=(
            ISO8601ZFormatter(),
            RelativePlFormatter(),
            RelativeEnFormatter(),
            SmartFormatter(),
            PolishHardFormatter(),
        )
    )