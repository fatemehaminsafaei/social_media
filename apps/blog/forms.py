from django import forms
from apps.blog.models.blog import Comment, Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'tags']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
