import os
import sys
import django
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from products.models import Product, Category
from django.utils.text import slugify


def create_categories():
    """Создает категории товаров"""
    categories = [
        {'name': 'Солод', 'slug': 'malt'},
        {'name': 'Хмель', 'slug': 'hops'},
        {'name': 'Дрожжи', 'slug': 'yeast'},
        {'name': 'Наборы', 'slug': 'kits'},
        {'name': 'Оборудование', 'slug': 'equipment'},
        {'name': 'Аксессуары', 'slug': 'accessories'},
    ]

    created_cats = {}
    for cat_data in categories:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name']}
        )
        created_cats[cat_data['slug']] = cat
        if created:
            print(f"✅ Создана категория: {cat.name}")
        else:
            print(f"⚠️  Категория уже существует: {cat.name}")

    return created_cats


def create_products(categories):
    """Создает продукты"""
    products_data = [
        # СОЛОД
        {
            'name': 'Caramel Malt',
            'slug': 'product-caramel-malt',
            'description': 'Карамельный солод для придания пиву сладкого карамельного вкуса и золотистого цвета. Идеально подходит для элей, портеров и стаутов.',
            'category_slug': 'malt',
            'price': 450.00,
            'stock': 100,
            'is_active': True,
        },
        {
            'name': 'Maris Otter Malt',
            'slug': 'product-maris-otter-malt',
            'description': 'Традиционный английский солод с насыщенным солодовым вкусом. Основной солод для многих британских стилей пива.',
            'category_slug': 'malt',
            'price': 520.00,
            'stock': 80,
            'is_active': True,
        },
        {
            'name': 'Pilsner Malt',
            'slug': 'product-pilsner-malt',
            'description': 'Светлый солод для пилснеров и других светлых лагеров. Дает чистый солодовый вкус и светло-золотистый цвет.',
            'category_slug': 'malt',
            'price': 480.00,
            'stock': 120,
            'is_active': True,
        },
        {
            'name': 'Unmalted Wheat',
            'slug': 'product-unmalted-wheat',
            'description': 'Немолотый ячмень для придания пиву пшеничного вкуса и мутности. Используется в бельгийских витбирах и немецких вайценбирах.',
            'category_slug': 'malt',
            'price': 380.00,
            'stock': 90,
            'is_active': True,
        },

        # ХМЕЛЬ
        {
            'name': 'Cascade Hops',
            'slug': 'product-cascade-hops',
            'description': 'Американский хмель с цитрусовыми и цветочными нотами. Идеален для American Pale Ale и IPA.',
            'category_slug': 'hops',
            'price': 320.00,
            'stock': 200,
            'is_active': True,
        },
        {
            'name': 'Centennial Hops',
            'slug': 'product-centennial-hops',
            'description': 'Универсальный американский хмель с цитрусовыми и хвойными ароматами. "Супер-каскад" с более высокой альфа-кислотностью.',
            'category_slug': 'hops',
            'price': 350.00,
            'stock': 150,
            'is_active': True,
        },
        {
            'name': 'Citra Hops',
            'slug': 'product-citra-hops',
            'description': 'Популярный хмель с сильными цитрусовыми и тропическими ароматами (лайм, манго, личи). Любимый хмель для NEIPA.',
            'category_slug': 'hops',
            'price': 420.00,
            'stock': 120,
            'is_active': True,
        },
        {
            'name': 'Mosaic Hops',
            'slug': 'product-mosaic-hops',
            'description': 'Хмель с комплексным ароматом: ягоды, цитрусы, тропические фрукты и травы. Отлично подходит для современных IPA.',
            'category_slug': 'hops',
            'price': 400.00,
            'stock': 130,
            'is_active': True,
        },
        {
            'name': 'Saaz Hops',
            'slug': 'product-saaz-hops',
            'description': 'Классический чешский благородный хмель с мягким пряным и травяным ароматом. Обязателен для традиционных пилснеров.',
            'category_slug': 'hops',
            'price': 380.00,
            'stock': 110,
            'is_active': True,
        },

        # ДРОЖЖИ
        {
            'name': 'Imperial Yeast',
            'slug': 'product-imperial-yeast',
            'description': 'Жидкие дрожжи высокого качества для различных стилей пива. Отличная жизнеспособность и чистая ферментация.',
            'category_slug': 'yeast',
            'price': 280.00,
            'stock': 80,
            'is_active': True,
        },
        {
            'name': 'Safale US-05 Yeast',
            'slug': 'product-safale-us05-yeast',
            'description': 'Американские сухие дрожжи для элей. Нейтральный профиль, подчеркивает хмелевые и солодовые ароматы.',
            'category_slug': 'yeast',
            'price': 180.00,
            'stock': 150,
            'is_active': True,
        },

        # НАБОРЫ
        {
            'name': 'West Coast IPA Kit',
            'slug': 'product-west-coast-ipa-kit',
            'description': 'Полный набор для приготовления West Coast IPA. Включает все необходимое: солод, хмель, дрожжи и инструкцию.',
            'category_slug': 'kits',
            'price': 2500.00,
            'stock': 30,
            'is_active': True,
        },
    ]

    created_count = 0
    existing_count = 0

    for product_data in products_data:
        # Получаем категорию
        category = categories.get(product_data['category_slug'])
        if not category:
            print(f"❌ Категория не найдена: {product_data['category_slug']}")
            continue

        # Создаем или обновляем продукт
        product, created = Product.objects.update_or_create(
            slug=product_data['slug'],
            defaults={
                'name': product_data['name'],
                'category': category,
                'description': product_data['description'],
                'price': product_data['price'],
                'stock': product_data['stock'],
                'is_active': product_data['is_active'],
            }
        )

        if created:
            created_count += 1
            print(f"✅ Создан продукт: {product.name} ({product.category.name}) - {product.price} руб.")
        else:
            existing_count += 1
            print(f"⚠️  Обновлен продукт: {product.name}")

    return created_count, existing_count


def main():
    print("=" * 60)
    print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ПРОДУКТАМИ")
    print("=" * 60)

    # Создаем категории
    print("\n1. Создание категорий...")
    categories = create_categories()

    # Создаем продукты
    print("\n2. Создание продуктов...")
    created, existing = create_products(categories)

    # Итоги
    print("\n" + "=" * 60)
    print("ИТОГИ:")
    print(f"✅ Создано новых продуктов: {created}")
    print(f"⚠️  Обновлено существующих: {existing}")
    print(f"📊 Всего продуктов в базе: {Product.objects.count()}")
    print(f"📁 Всего категорий в базе: {Category.objects.count()}")
    print("\nДля просмотра в админке: http://127.0.0.1:8000/admin/")
    print("=" * 60)


if __name__ == "__main__":
    main()