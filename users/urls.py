# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация
    path('register/', views.RegisterView.as_view(), name='register'),

    # Вход
    path('login/', views.custom_login_view, name='login'),

    # Выход
    path('logout/', views.logout_view, name='logout'),

    # Профиль
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Account
    path('account/', views.AccountView.as_view(), name='account'),

    # Забыли пароль - ДОБАВЬТЕ ЭТО!
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='forgot_password.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/accounts/password-reset/done/'
    ), name='forgot_password'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]