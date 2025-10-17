# scraper/infra/repository.py
from django.db import IntegrityError
from scraper.models import Article
from scraper.domain.models import ArticleData

class DjangoArticleRepository:
    def exists(self, url: str) -> bool:
        return Article.objects.filter(url=url).exists()

    def save(self, a: ArticleData) -> None:
        try:
            Article.objects.create(
                url=a.url,
                title=a.title,
                content=a.content_html,
                cleaned_content=a.content_text,
                date=a.published_at,
            )
        except IntegrityError:
            # ignorujemy duplikaty (lub podnieś wyjątek, jeśli wolisz)
            pass
