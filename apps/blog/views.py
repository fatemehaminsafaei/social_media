import sys

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from apps.blog.models import Post, Preference, Comment
from apps.blog.forms import NewCommentForm
from apps.users.models import Follow


def is_users(post_user, logged_user):
    return post_user == logged_user


PAGINATION_COUNT = 3


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATION_COUNT

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        all_users = []
        data_counter = Post.objects.values('author') \
                           .annotate(author_count=Count('author')) \
                           .order_by('-author_count')[:6]
        for aux in data_counter:
            all_users.append(User.objects.filter(pk=aux['author'].first()))
        data['preference'] = Preference.objects.all()
        data['all_users'] = all_users
        print(all_users, file=sys.stderr)
        return data

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Post.objects.filter(author__in=follows).order_by('-date_posted')



def about(request):
    return render(request,'blog/about.html',)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)
        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)
        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follow_between = Follow.objects.filter(user=request.user,
                                                   follow_user=self.visible_user())
            if 'follow' in request.POST:
                new_relation = Follow(user=request.user, follow_user=self.visible_user())
                if follow_between.count() == 0:
                    new_relation.save()
            elif 'unfollow' in request.POST:
                if follow_between.count() > 0:
                    follow_between.delete()
        return self.get(self, request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comment_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['commenrs'] = comment_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)