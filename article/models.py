import django.utils.timezone as timezone
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
# Create your models here.
from mdeditor.fields import MDTextField


class NavBar(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    parent_id = models.IntegerField(blank=True, null=True)
    sort = models.IntegerField()




class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    total_views = models.PositiveIntegerField(default=0)
    content = MDTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created_at',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        print("调用了获取文章地址的方法")
        return reverse('article:article_detail_show', args=[self.id])











