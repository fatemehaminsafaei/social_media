from django.contrib import admin
from apps.users.models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'follow_user', 'date']

# admin.site.register(Profile)
# admin.site.register(Follow)
