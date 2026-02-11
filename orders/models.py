from django.conf import settings
from django.db import models

from products.models import Product

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = [
    ('debit', 'Debit Card'),
    ('credit', 'Credit Card'),
    ('cash', 'Cash on Delivery'),
    ('paypal', 'PayPal'),
    ('wallet', 'Digital Wallet'),
]

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Контактная информация
    full_name = models.CharField(max_length=100, default="")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, default="")

    # Адрес доставки
    city = models.CharField(max_length=100, default="")
    address = models.TextField(default="")
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    # Способ оплаты
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='debit'
    )

    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Статус оплаты
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity