from django.contrib import admin

# Register your models here.
# 别忘了导入ArticlerPost
from .models import Post

# 注册ArticlePost到admin中
admin.site.register(Post)
