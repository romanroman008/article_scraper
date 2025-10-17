# scraper/infra/parser.py
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.parser_chain import extract_date_from_soup
from scraper.infrastructure.parsing.parsing_utils import pick_title, pick_container, html_to_text

from scraper.domain.models import ArticleData



class BeautifulSoupArticleParser:
    def parse(self, url: str, html: str) -> ArticleData:
        soup = BeautifulSoup(html, "html.parser")

        title = pick_title(soup)
        container = pick_container(soup)
        content_html = str(container) if container else html
        content_text = html_to_text(content_html)

        raw_date = extract_date_from_soup(soup)  # -> str | None
        published_at = raw_date

        return ArticleData(
            url=url,
            title=title,
            content_html=content_html,
            content_text=content_text,
            published_at=published_at,
            source_domain=urlparse(url).netloc,
        )
