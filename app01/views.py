from django.shortcuts import render
from .models import NavBar
# Create your views here.

# 获取Nav_bar
def view(request):
    nav_bar_list = NavBar.objects.all()  # 查询所有用户
    for item in nav_bar_list:
        print(item.name,item.url)
    return render(request,"index.html",{"nav_bar_list":nav_bar_list})