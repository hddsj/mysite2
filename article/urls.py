# 作者: hxd
# 2023年06月02日18时55分04秒
from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    # 写文章
    path('article-create/', views.article_create, name='article_create'),
    # 展示文章详情
    path('article-detail-show/<int:id>/', views.article_detail, name='article_detail_show'),
    # 删除文章
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),

    path('article-list/',views.view,name = 'article_list'),

    path('show_articles_page_by_type/',views.show_articles_page_by_type,name = 'show_articles_page_by_type'),

    path('happen/', views.article_list, {'type': 'happen'}, name='happen'),
    path('prevent/', views.article_list, {'type': 'prevent'}, name='prevent'),
    path('appliance/', views.article_list,  {'type': 'appliance'},name='appliance'),
    path('news/', views.article_list,  {'type': 'news'},name='news'),
    path('about/', views.article_list,  {'type': 'about'},name='about'),
    # 更新文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),

]