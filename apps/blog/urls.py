from rest_framework import routers
from . import views
from django.conf.urls.static import static
from django.urls import path, include
from apps.blog.views import PostListView, UserPostListView, PostDetailView, PostCreateView, PostUpdateView, \
    FollowsListView, FollowersListView, PostDeleteView, postpreference, post_list, CommentDeleteView, CommentUpdateView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/del/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/comment/del/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comment/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:postid>/preference/<int:userpreference>', postpreference, name='postpreference'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/follows', FollowsListView.as_view(), name='user-follows'),
    path('user/<str:username>/followers', FollowersListView.as_view(), name='user-followers'),
    path('l/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/posts', post_list)
]
