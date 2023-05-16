from django.shortcuts import render
from .models import NavBar,Post
# Create your views here.

# 获取Nav_bar
def view(request):
    # 查询所有导航栏分类
    nav_bar_list = NavBar.objects.all()
    # 查询发布的文章
    article_list = Post.objects.all()
    print(article_list[0].url)
    return render(request,"index2.html",{"nav_bar_list":nav_bar_list,"article_list":article_list})
