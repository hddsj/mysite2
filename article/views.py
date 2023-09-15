from django.shortcuts import render,redirect
from django.template import RequestContext

from comment.models import Comment
from .models import NavBar,Post,ArticleColumn
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
from django.contrib.auth.models import User
# 引入markdown模块
import markdown
from django.core.paginator import Paginator
# Create your views here.
def show_article_list():
    # 查询发布的文章
    article_list = Post.objects.all()
    # 将文章按照模块分类
    happen_article_list = []  # 近视的发生
    prevent_article_list = []  # 近视的预防
    appliance_article_list = []  # 防近视的器材
    news_article_list = []  # 防近视要闻
    for item in article_list:
        if item.column.title == "防近视要闻":
            news_article_list.append(item)
        elif item.column.title == "防近视器材":
            appliance_article_list.append(item)
        elif item.column.title == "近视的预防":
            prevent_article_list.append(item)
        elif item.column.title == "近视的发生":
            happen_article_list.append(item)

    # 最多只显示前8条数据
    happen_article_list_len = len(happen_article_list) if len(happen_article_list) <= 8 else 8
    prevent_article_list_len = len(prevent_article_list) if len(prevent_article_list) <= 8 else 8
    appliance_article_list_len = len(appliance_article_list) if len(appliance_article_list) <= 8 else 8
    news_article_list_len = len(news_article_list) if len(news_article_list) <= 8 else 8
    happen_article_sub_list = happen_article_list[:happen_article_list_len]
    prevent_article_sub_list = prevent_article_list[:prevent_article_list_len]
    appliance_article_sub_list = appliance_article_list[:appliance_article_list_len]
    news_article_sub_list = news_article_list[:news_article_list_len]
    return [happen_article_sub_list,prevent_article_sub_list,appliance_article_sub_list,news_article_sub_list]
# 获取Nav_bar
def view(request):
    happen_article_sub_list,prevent_article_sub_list,appliance_article_sub_list,news_article_sub_list = show_article_list()
    return render(request, "home.html", {"happen_article_sub_list":happen_article_sub_list,
                                         "prevent_article_sub_list": prevent_article_sub_list,
                                         "appliance_article_sub_list": appliance_article_sub_list,
                                         "news_article_sub_list": news_article_sub_list})


def article_detail(request,id):
    if request.user.is_authenticated:
        logged_in = True
        username = request.session.get('username', None)
    else:
        logged_in = False
        username = '请登录：'
    # 查询所有导航栏分类
    nav_bar_list = ArticleColumn.objects.all()
    # 取出相应的文章
    article = Post.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    author_name = User.objects.get(id = article.author_id)
    # 将markdown语法渲染成html样式
    article.content = markdown.markdown(article.content.replace("\r\n", '  \n'),
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',],
                                        safe_mode = True,
                                        enable_attributes=False)
    #取出文章评论
    comments_list = Comment.objects.filter(article=id)

    # 每页显示 5条评论
    paginator = Paginator(comments_list, 5)

    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    comments = paginator.get_page(page)


    return render(request, "article.html",{"article":article,
                                           "username": username,
                                           "logged_in": logged_in,
                                           "author":author_name,
                                           'comments_list':comments_list,
                                           'comments': comments,
                                           'nav_bar_list':nav_bar_list})

def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            return redirect("/")
        else:
            for field in article_post_form:
                for error in field.errors:
                    # 显示错误信息
                    print(field.label, error)
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form,'columns':columns}
        # 返回模板
        return render(request, 'editor.html', context)

# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = Post.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

def show_articles_page_by_type(request):
    # 获取文章的id
    id = request.GET.get("id")

    # 查询所有导航栏分类
    nav_bar_list = ArticleColumn.objects.all()
    # 查询发布的文章
    article_list = Post.objects.filter(column_id=id)
    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 15)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 赋值上下文
    context = {"nav_bar_list":nav_bar_list,
               'article_list': articles}
    # 返回模板
    return render(request, 'article_list.html', context)



def article_list(request,type):
    if type == 'home':
        pass
    # 返回主页
    elif type == 'happen':
        article_list = Post.objects.filter(column_id=1)
    elif type == 'prevent':
        article_list = Post.objects.filter(column_id=2)
    elif type == 'appliance':
        article_list = Post.objects.filter(column_id=3)
    elif type == 'news':
        article_list = Post.objects.filter(column_id=4)
    else:
        pass
    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 1)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 赋值上下文
    context = {'articles': articles}
    # 返回模板
    return render(request, 'article_list.html', context)


def article_update(request,id):
    article = Post.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data = request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return redirect("article:article_detail_show",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 文章分类
        columns = ArticleColumn.objects.all()
        type = columns[article.column_id].title
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'columns':columns,
                   "type":type}
        # 将响应返回到模板中
        return render(request, 'editor.html', context)

