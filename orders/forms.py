from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    # Существующие поля
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'John Doe'}),
        label='Full Name'
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': '+1 (555) 123-4567'}),
        label='Phone Number'
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': 'New York'}),
        label='City'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'Textarea', 'placeholder': '123 Main St, Apt 4B'}),
        label='Shipping Address'
    )

    # ДОБАВЬТЕ ЭТИ ПОЛЯ
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'john@example.com'}),
        label='Email (optional)'
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'Input', 'placeholder': '10001'}),
        label='Postal Code (optional)'
    )

    # ДОБАВЬТЕ ВЫБОР СПОСОБА ОПЛАТЫ
    PAYMENT_METHOD_CHOICES = [
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
        ('cash', 'Cash on Delivery'),
        ('paypal', 'PayPal'),
        ('wallet', 'Digital Wallet'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='debit',
        label='Payment Method'
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'city', 'address', 'postal_code',
            'payment_method'
        ]