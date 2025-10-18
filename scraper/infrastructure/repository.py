import logging
from django.db import IntegrityError, DatabaseError
from scraper.domain.models import ArticleData
from scraper.models import Article


class DjangoArticleRepository:
    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(type(self).__name__)

    def exists(self, url: str) -> bool:
        return Article.objects.filter(url=url).only("pk").exists()

    def save(self, a: ArticleData) -> None:
        try:
            obj = Article.objects.create(
                url=a.url,
                title=a.title,
                content=a.content_html,
                cleaned_content=a.content_text,
                date=a.published_at,
            )
            self.log.info(
                "Zapisano artykuł (id=%s, url=%s, title_len=%d, text_len=%d, has_date=%s).",
                getattr(obj, "id", None),
                a.url,
                len(a.title or ""),
                len(a.content_text or ""),
                bool(a.published_at),
            )

        except IntegrityError as e:
            self.log.info("Pominięto zapis – artykuł już istnieje (url=%s).", a.url)


        except DatabaseError:

            self.log.error("Błąd bazy danych podczas zapisu artykułu (url=%s).", a.url, exc_info=True)
            raise

        except Exception:
            self.log.error("Nieoczekiwany błąd podczas zapisu artykułu (url=%s).", a.url, exc_info=True)
            raise
