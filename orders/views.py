"""Views для управления корзиной покупок."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from django.conf import settings
from products.models import Product

from .cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CartView(View):
    """Отображение содержимого корзины."""
    template_name = 'cart.html'

    def get(self, request):
        cart = Cart(request)

        cart_items = []
        for item in cart:
            cart_items.append({
                'product': item['product'],
                'quantity': item['quantity'],
                'price': item['price'],
                'total_price': item['total_price'],
            })

        context = {
            'cart_items': cart_items,
            'total_price': cart.get_total_price(),
            'items_count': len(cart),
        }

        return render(request, self.template_name, context)


class OrderCreateView(LoginRequiredMixin, View):
    """Создание заказа (только для авторизованных пользователей)."""

    def get(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            return redirect('orders:cart')

        if not request.user.is_authenticated:
            request.session['cart_before_login'] = cart.copy()
            request.session.modified = True
            request.session.save()

            return redirect(f"{settings.LOGIN_URL}?next={reverse('orders:checkout')}")

        form = OrderCreateForm()
        return render(request, 'checkout.html', {'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)

        if len(cart) == 0:
            return redirect('orders:cart')

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = cart.get_total_price()
                    order.save()

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item['product'],
                            price=item['price'],
                            quantity=item['quantity']
                        )
                        # Уменьшаем запас
                        product = item['product']
                        if product.stock < item['quantity']:
                            raise ValueError(f"Not enough stock for {product.name}")
                        product.stock -= item['quantity']
                        product.save()

                    cart.clear()
                    messages.success(request, f'Order #{order.id} created!')
                    return render(request, 'order_created.html', {'order': order})

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('orders:cart')

        return render(request, 'checkout.html', {'cart': cart, 'form': form})


@require_POST
def cart_add(request, product_id: int):
    import sys
    from decimal import Decimal

    print("\n🔍 CART ADD", file=sys.stderr)
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    print(f"  Product: {product.name}, price: {product.price} ({type(product.price)})", file=sys.stderr)

    result = cart.add(product=product, quantity=quantity)

    print(f"  Result: {result}", file=sys.stderr)
    print(f"  Cart now has {len(cart)} items", file=sys.stderr)

    return JsonResponse({
        'status': result['status'],
        'message': result['message'],
        'cart_items_count': len(cart),
        'cart_total': str(cart.get_total_price()),
    })


@require_POST
def cart_remove(request, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f'{product.name} removed from cart',
            'cart_items_count': len(cart),
            'cart_total': str(cart.get_total_price()),
        })
    return redirect('orders:cart')


@require_POST
def cart_update(request, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    result = cart.update(product=product, quantity=quantity)

    return JsonResponse({
        'status': result['status'],
        'message': result['message'],
        'cart_items_count': len(cart),
        'cart_total': str(cart.get_total_price()),
        'item_total': str(product.price * quantity) if quantity > 0 else '0',
    })


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Cart cleared')
    return redirect('orders:cart')


@require_POST
def save_cart_before_login(request):
    """
    Сохраняет корзину в сессию перед редиректом на логин.
    """
    import sys

    print("\n" + "=" * 50, file=sys.stderr)
    print("🔍 SAVE CART BEFORE LOGIN CALLED", file=sys.stderr)

    cart = Cart(request)
    print(f"Cart has {len(cart)} items", file=sys.stderr)

    if len(cart) > 0:
        # ✅ ИСПОЛЬЗУЕМ copy() - гарантированно JSON-сериализуемые данные!
        cart_data = cart.copy()
        request.session['cart_before_login'] = cart_data
        request.session.modified = True
        request.session.save()

        print(f"✅ Cart saved with {len(cart_data)} items", file=sys.stderr)
        print(f"Session ID: {request.session.session_key}", file=sys.stderr)
        print(f"Data type: {type(cart_data)}", file=sys.stderr)

        # Проверяем тип price
        if cart_data:
            sample_id = list(cart_data.keys())[0]
            sample_price = cart_data[sample_id]['price']
            print(f"Sample price type: {type(sample_price)} - {sample_price}", file=sys.stderr)

        return JsonResponse({
            'status': 'success',
            'message': f'Cart saved with {len(cart)} items',
            'cart_items_count': len(cart)
        })

    print("⚠️ Cart is empty", file=sys.stderr)
    return JsonResponse({
        'status': 'empty',
        'message': 'Cart is empty'
    })


@extend_schema_view(
    list=extend_schema(description="Получить список всех заказов текущего пользователя."),
    retrieve=extend_schema(description="Получить детали конкретного заказа.")
)
class OrderViewSet(viewsets.ModelViewSet):
    """API для управления заказами текущего пользователя."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)