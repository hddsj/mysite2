import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.
from article.models import Post
from comment.forms import CommentForm
from django.http import HttpResponse

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id):
    article = get_object_or_404(Post, id=article_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        return HttpResponse("仅接受POST请求")
