# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'Input',
            'placeholder': 'Enter your email address'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'Input',
            'placeholder': 'Enter your phone number (optional)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'Input',
                'placeholder': 'Choose a unique username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомные placeholder для полей пароля
        self.fields['password1'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'Input',
            'placeholder': 'Confirm your password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email or try logging in.")
        return email.lower()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Используем Django's встроенную валидацию пароля
        validate_password(password1)
        return password1


# Если хотите ослабить требования к паролю для тестирования:
class RegisterFormTest(UserCreationForm):
    """Упрощенная форма для тестирования (меньше требований к паролю)"""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email.lower()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Убираем сложные проверки пароля
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:  # Минимум 3 символа вместо 8
            raise ValidationError("Password must be at least 3 characters long.")
        return password1