from django.db import models
from rest_framework import serializers


# Create your models here.
class Article(models.Model):
    title = models.CharField()
    content = models.TextField()
    cleaned_content = models.TextField()
    url = models.URLField()
    date = models.TextField()


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "url", "title", "content", "cleaned_content", "date"
        ]