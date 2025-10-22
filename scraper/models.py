from django.db import models
from rest_framework import serializers


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    cleaned_content = models.TextField()
    url = models.URLField(unique=True)
    date = models.DateTimeField(null=True, blank=True)



class ArticleSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = [
            "url", "title", "content", "cleaned_content", "date" , "source"
        ]

    def get_source(self, obj):
        from urllib.parse import urlparse
        return urlparse(obj.url).netloc