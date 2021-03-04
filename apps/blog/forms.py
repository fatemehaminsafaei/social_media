from django import forms
from apps.blog.models import Comment


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']