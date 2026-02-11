# users/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView

from orders.models import Order
from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Сохраняем пользователя и входим"""
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, 'Registration successful! Welcome to Hop & Barley.')

        # 👇 ВАЖНО: проверяем next параметр после регистрации
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return response

    def form_invalid(self, form):
        """Обработка ошибок формы"""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        """Если пользователь уже авторизован, перенаправляем"""
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in.')
            return redirect('home')
        return super().get(request, *args, **kwargs)


def custom_login_view(request):
    """Простой кастомный view для входа с поддержкой next параметра"""
    # Если пользователь уже авторизован, перенаправляем
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')

    # 👇 ПОЛУЧАЕМ next URL ИЗ GET ПАРАМЕТРОВ
    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')

            # 👇 ВАЖНО: перенаправляем на сохраненный next URL
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    # Передаем next_url в контекст шаблона
    return render(request, 'login.html', {'next': next_url})


@require_POST
def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')
        return context


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Загружаем заказы ТОЛЬКО текущего пользователя
        context['orders'] = Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
        return context

    def post(self, request):
        """Обновление информации пользователя"""
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        # Смена пароля
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password changed successfully. Please login again.')
            return redirect('users:login')

        messages.success(request, 'Account information updated successfully!')
        return redirect('users:account')