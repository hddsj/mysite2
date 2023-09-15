from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#文章的评论
from article.models import Post


class Comment(models.Model):
    article = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_time',)
    def __str__(self):
        return self.body[:30]