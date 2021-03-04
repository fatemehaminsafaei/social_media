from django.contrib import admin
from apps.blog.models import Post, Comment, Preference


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'date_posted', 'author', 'likes', 'dislikes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'date_posted', 'author', 'post_connected']


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'value', 'date']
