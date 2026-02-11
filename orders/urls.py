from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Основные страницы
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.OrderCreateView.as_view(), name='checkout'),

    # API операции с корзиной
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('cart/save-before-login/', views.save_cart_before_login, name='save_cart_before_login'),
]