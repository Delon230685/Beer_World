from django.utils.deprecation import MiddlewareMixin
from decimal import Decimal


class CartTransferMiddleware(MiddlewareMixin):
    """Middleware для переноса корзины из анонимной сессии в авторизованную."""

    def process_request(self, request):
        # Переносим корзину сразу после авторизации
        if request.user.is_authenticated:
            # Проверяем все возможные ключи
            saved_cart = None
            for key in ['cart_before_login', 'saved_cart', 'cart_backup']:
                if key in request.session:
                    saved_cart = request.session.pop(key)
                    print(f"🔄 Found cart in session key '{key}' with {len(saved_cart)} items")
                    break

            if saved_cart:
                from .cart import Cart
                cart = Cart(request)

                before_count = len(cart)
                print(f"🔄 Cart before transfer: {before_count} items")

                # Переносим товары
                for product_id_str, item_data in saved_cart.items():
                    from products.models import Product
                    try:
                        product_id = int(product_id_str)
                        product = Product.objects.get(id=product_id, is_active=True)

                        # ВАЖНО: проверяем тип price
                        if 'price' in item_data and isinstance(item_data['price'], Decimal):
                            item_data['price'] = str(item_data['price'])
                            print(f"  ⚠️ Конвертирован Decimal в строку: {item_data['price']}")

                        cart.add(product=product, quantity=item_data['quantity'])
                        print(f"  ✅ Added {product.name} x{item_data['quantity']}")
                    except Exception as e:
                        print(f"  ❌ Error adding product {product_id_str}: {e}")

                after_count = len(cart)
                print(f"🔄 Cart after transfer: {after_count} items")
                request.session.modified = True

        return None


class ForceDecimalToStringMiddleware(MiddlewareMixin):
    """
    ПРИНУДИТЕЛЬНО конвертирует все Decimal в строки в сессии.
    Добавьте этот middleware ПОСЛЕ SessionMiddleware.
    """

    def process_response(self, request, response):
        # После обработки запроса, перед отправкой ответа
        if hasattr(request, 'session') and request.session:
            modified = False

            # Проверяем все ключи в сессии
            session_keys = list(request.session.keys())

            for key in session_keys:
                # Нас интересуют только ключи, связанные с корзиной
                if key in ['cart', 'cart_before_login', 'saved_cart', 'cart_backup']:
                    value = request.session.get(key)

                    # Рекурсивно конвертируем все Decimal в строки
                    if isinstance(value, dict):
                        new_value = self._convert_decimals_to_strings(value)
                        if new_value != value:
                            request.session[key] = new_value
                            modified = True
                            print(f"🛡️ MIDDLEWARE: Конвертированы Decimal в {key}")

            if modified:
                request.session.modified = True

        return response

    def _convert_decimals_to_strings(self, obj):
        """Рекурсивно конвертирует все Decimal в строки."""
        if isinstance(obj, dict):
            return {k: self._convert_decimals_to_strings(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_decimals_to_strings(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_decimals_to_strings(i) for i in obj)
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return obj