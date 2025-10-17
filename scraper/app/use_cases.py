# scraper/app/use_cases.py
import logging
import traceback
from typing import Iterable, List, Optional

from requests import HTTPError

from scraper.domain.ports import HtmlFetcher, Renderer, ArticleParser, ArticleRepository
from scraper.exporters.json_exporter import JsonExporter


class ScrapeArticlesUseCase:
    def __init__(self,
                 fetcher: HtmlFetcher,
                 parser: ArticleParser,
                 repository: ArticleRepository,
                 renderer: Optional[Renderer] = None,
                 min_text_len: int = 150):
        self.fetcher = fetcher
        self.parser = parser
        self.repository = repository
        self.renderer = renderer
        self.min_text_len = min_text_len

    def run(self, urls: Iterable[str]) -> dict:
        created = 0; skipped = 0; failed = 0
        articles = []
        i = 0
        total = len(urls)
        for url in urls:
            i+=1
            try:
                logging.info(f"Scraping {i}/{total} article with url: {url}...")
                # if self.repository.exists(url):
                #     skipped += 1; continue

                html = self.fetcher.fetch(url)
                article = self.parser.parse(url, html)



                if self.renderer and (not article.content_text or len(article.content_text) < self.min_text_len):
                    rendered_html = self.renderer.render(url)
                    article = self.parser.parse(url, rendered_html)

                self.repository.save(article)
                articles.append(article)

                created += 1
            except Exception as e:
                failed += 1
                logging.error("url=%s reason=%s", url, e)

                continue

        exporter = JsonExporter()
        exporter.export(articles, "out/articles.json")
        return {"created": created, "skipped": skipped, "failed": failed}
