"""
Модуль корзины для управления товарами в сессии пользователя.
"""
from decimal import Decimal
from typing import Dict, Iterator, Any

from django.conf import settings

from products.models import Product


class Cart:
    """
    Класс для управления корзиной покупок в сессии Django.
    В сессии ВСЕГДА хранятся только JSON-сериализуемые типы.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False) -> Dict[str, str]:
        import sys

        product_id = str(product.id)
        print(f"  Cart.add: {product.name}, qty={quantity}", file=sys.stderr)

        if quantity > product.stock:
            return {
                'status': 'error',
                'message': f'Available stock: {product.stock}. Cannot add {quantity} items.'
            }

        if product_id not in self.cart:
            print(f"    Новый товар, price={product.price} ({type(product.price)})", file=sys.stderr)
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # КОНВЕРТИРУЕМ В СТРОКУ!
            }
            print(f"    Сохранено как: {self.cart[product_id]['price']} ({type(self.cart[product_id]['price'])})",
                  file=sys.stderr)

        if override_quantity:
            new_quantity = quantity
        else:
            new_quantity = self.cart[product_id]['quantity'] + quantity

        if new_quantity > product.stock:
            return {
                'status': 'error',
                'message': f'Cannot add more. Maximum available: {product.stock}'
            }

        self.cart[product_id]['quantity'] = new_quantity
        self.save()

        return {
            'status': 'success',
            'message': f'{product.name} added to cart'
        }

    def remove(self, product: Product) -> None:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product: Product, quantity: int) -> Dict[str, str]:
        if quantity <= 0:
            self.remove(product)
            return {
                'status': 'success',
                'message': 'Item removed from cart'
            }
        return self.add(product, quantity, override_quantity=True)

    def save(self) -> None:
        """Сохранить корзину в сессии - ПРИНУДИТЕЛЬНАЯ КОНВЕРТАЦИЯ!"""
        from decimal import Decimal

        # Конвертируем ВСЕ Decimal в строки
        for product_id, item in self.cart.items():
            for key, value in list(item.items()):
                if isinstance(value, Decimal):
                    self.cart[product_id][key] = str(value)

        self.session.modified = True

    def clear(self) -> None:
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """
        Итерация по товарам в корзине.
        ТОЛЬКО ДЛЯ ЧТЕНИЯ - НИЧЕГО НЕ СОХРАНЯЕТ!
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        # СОЗДАЁМ НОВЫЙ СЛОВАРЬ ДЛЯ ИТЕРАЦИИ
        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                yield {
                    'product': product,
                    'quantity': self.cart[product_id]['quantity'],
                    'price': Decimal(self.cart[product_id]['price']),
                    'total_price': Decimal(self.cart[product_id]['price']) * self.cart[product_id]['quantity']
                }

    def __len__(self) -> int:
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """Вернуть Decimal для использования в коде"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_items_count(self) -> int:
        return len(self.cart)

    def copy(self):
        """Создать копию корзины - все данные уже JSON-сериализуемы"""
        import copy
        return copy.deepcopy(self.cart)