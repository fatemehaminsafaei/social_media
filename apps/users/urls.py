from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView
from django.urls import path
from . import views

# from users import views as users_views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password-reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password-reset-done'),
    path('register/', views.register, name='register-users'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.SearchView, name='search'),
]
