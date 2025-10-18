from django.shortcuts import render
from rest_framework import viewsets


from scraper.models import Article, ArticleSerializer


# Create your views here.


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/articles/        -> lista
    GET /api/articles/{id}/   -> szczegół
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



    def get_queryset(self):
        queryset = super().get_queryset()
        source = self.request.query_params.get("source")

        if source:
            # Filtrowanie po domenie źródłowej w URL
            # Używamy icontains, aby dopasować np. subdomeny (np. "www.domain.com")
            queryset = queryset.filter(url__icontains=source)

        return queryset