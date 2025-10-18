
import logging

from typing import Iterable, List, Optional

from requests import HTTPError

from scraper.domain.ports import HtmlFetcher, Renderer, ArticleParser, ArticleRepository



class ScrapeArticlesUseCase:
    def __init__(
        self,
        fetcher: HtmlFetcher,
        parser: ArticleParser,
        repository: ArticleRepository,
        renderer: Optional[Renderer] = None,
        min_text_len: int = 150,
    ):
        self.fetcher = fetcher
        self.parser = parser
        self.repository = repository
        self.renderer = renderer
        self.min_text_len = min_text_len

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def run(self, urls: Iterable[str]):
        created = skipped = failed = 0
        articles = []


        try:
            total = len(urls)
        except Exception:
            total = None

        self.log.info(
            "Rozpoczęto scrapowanie artykułów (liczba_url=%s, min_text_len=%d).",
            total if total is not None else "nieznana",
            self.min_text_len,
        )

        i = 0
        for url in urls:
            i += 1
            try:
                self.log.info(
                    "Przetwarzanie URL (%s/%s): %s",
                    i,
                    total if total is not None else "?",
                    url,
                )

                if self.repository.exists(url):
                    skipped += 1
                    self.log.info("Pominięto istniejący artykuł (url=%s).", url)
                    continue


                html = self.fetcher.fetch(url)


                article = self.parser.parse(url, html)


                needs_render_fallback = (
                    self.renderer is not None
                    and (not article.content_text or len(article.content_text) < self.min_text_len)
                )
                if needs_render_fallback:
                    self.log.info(
                        "Wywołano fallback renderowania (url=%s, text_len=%d < %d).",
                        url,
                        len(article.content_text or ""),
                        self.min_text_len,
                    )
                    rendered_html = self.renderer.render(url)
                    article = self.parser.parse(url, rendered_html)

                self.repository.save(article)
                articles.append(article)
                created += 1

                self.log.info(
                    "Zapisano artykuł (url=%s, title_len=%d, text_len=%d, has_date=%s).",
                    url,
                    len(article.title or ""),
                    len(article.content_text or ""),
                    bool(article.published_at),
                )

            except HTTPError as e:
                failed += 1
                status = getattr(e.response, "status_code", None)
                self.log.error(
                    "Błąd HTTP podczas pobierania (url=%s, status=%s, reason=%s).",
                    url,
                    status,
                    str(e),
                )
                continue

            except Exception:
                failed += 1
                self.log.error("Błąd podczas przetwarzania URL (url=%s).", url, exc_info=True)
                continue


        self.log.info(
            "Zakończono scrapowanie (created=%d, skipped=%d, failed=%d, total=%s).",
            created,
            skipped,
            failed,
            total if total is not None else i,
        )
