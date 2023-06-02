# 作者: hxd
# 2023年06月02日18时55分04秒
from django.urls import path
from . import views
app_name = 'app01'

urlpatterns = [
    path('',views.show_article,name = 'article')
]