# 作者: hxd
# 2023年07月13日10时55分36秒
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']