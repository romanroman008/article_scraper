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


