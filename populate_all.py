# populate_all.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from products.models import Product, Category


def create_categories():
    """Создает категории"""
    print("📁 СОЗДАНИЕ КАТЕГОРИЙ")
    print("-" * 40)

    categories_data = [
        {'name': 'Солод', 'slug': 'malt'},
        {'name': 'Хмель', 'slug': 'hops'},
        {'name': 'Дрожжи', 'slug': 'yeast'},
        {'name': 'Наборы', 'slug': 'kits'},
        {'name': 'Оборудование', 'slug': 'equipment'},
        {'name': 'Аксессуары', 'slug': 'accessories'},
    ]

    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name']}
        )
        categories[cat_data['slug']] = cat
        print(f"{'✅ Создана' if created else '⚠️  Уже есть'} категория: {cat.name}")

    return categories


def create_products(categories):
    """Создает продукты"""
    print("\n🛒 СОЗДАНИЕ ПРОДУКТОВ")
    print("-" * 40)

    products_data = [
        # СОЛОД
        {
            'name': 'Caramel Malt 60L',
            'slug': 'product-caramel-malt',
            'description': 'Карамельный солод для придания пиву сладкого карамельного вкуса и золотистого цвета. Идеально подходит для элей, портеров и стаутов.',
            'category_slug': 'malt',
            'price': 450.00,
            'stock': 100,
        },
        {
            'name': 'Maris Otter Pale Malt',
            'slug': 'product-maris-otter-malt',
            'description': 'Традиционный английский солод с насыщенным солодовым вкусом. Основной солод для многих британских стилей пива.',
            'category_slug': 'malt',
            'price': 520.00,
            'stock': 80,
        },
        {
            'name': 'Pilsner Malt',
            'slug': 'product-pilsner-malt',
            'description': 'Светлый солод для пилснеров и других светлых лагеров. Дает чистый солодовый вкус и светло-золотистый цвет.',
            'category_slug': 'malt',
            'price': 480.00,
            'stock': 120,
        },
        {
            'name': 'Unmalted Wheat',
            'slug': 'product-unmalted-wheat',
            'description': 'Немолотый ячмень для придания пиву пшеничного вкуса и мутности. Используется в бельгийских витбирах и немецких вайценбирах.',
            'category_slug': 'malt',
            'price': 380.00,
            'stock': 90,
        },

        # ХМЕЛЬ
        {
            'name': 'Cascade Hops',
            'slug': 'product-cascade-hops',
            'description': 'Американский хмель с цитрусовыми и цветочными нотами. Идеален для American Pale Ale и IPA.',
            'category_slug': 'hops',
            'price': 320.00,
            'stock': 200,
        },
        {
            'name': 'Centennial Hops',
            'slug': 'product-centennial-hops',
            'description': 'Универсальный американский хмель с цитрусовыми и хвойными ароматами. "Супер-каскад" с более высокой альфа-кислотностью.',
            'category_slug': 'hops',
            'price': 350.00,
            'stock': 150,
        },
        {
            'name': 'Citra Hops',
            'slug': 'product-citra-hops',
            'description': 'Популярный хмель с сильными цитрусовыми и тропическими ароматами (лайм, манго, личи). Любимый хмель для NEIPA.',
            'category_slug': 'hops',
            'price': 420.00,
            'stock': 120,
        },
        {
            'name': 'Mosaic Hops',
            'slug': 'product-mosaic-hops',
            'description': 'Хмель с комплексным ароматом: ягоды, цитрусы, тропические фрукты и травы. Отлично подходит для современных IPA.',
            'category_slug': 'hops',
            'price': 400.00,
            'stock': 130,
        },
        {
            'name': 'Saaz Hops',
            'slug': 'product-saaz-hops',
            'description': 'Классический чешский благородный хмель с мягким пряным и травяным ароматом. Обязателен для традиционных пилснеров.',
            'category_slug': 'hops',
            'price': 380.00,
            'stock': 110,
        },

        # ДРОЖЖИ
        {
            'name': 'Imperial Organic Yeast A07',
            'slug': 'product-imperial-yeast',
            'description': 'Жидкие дрожжи высокого качества для различных стилей пива. Отличная жизнеспособность и чистая ферментация.',
            'category_slug': 'yeast',
            'price': 280.00,
            'stock': 80,
        },
        {
            'name': 'SafAle US-05 Dry Ale Yeast',
            'slug': 'product-safale-us05-yeast',
            'description': 'Американские сухие дрожжи для элей. Нейтральный профиль, подчеркивает хмелевые и солодовые ароматы.',
            'category_slug': 'yeast',
            'price': 180.00,
            'stock': 150,
        },

        # НАБОРЫ
        {
            'name': 'West Coast IPA - All-Grain Kit',
            'slug': 'product-west-coast-ipa-kit',
            'description': 'Полный набор для приготовления West Coast IPA. Включает все необходимое: солод, хмель, дрожжи и подробную инструкцию.',
            'category_slug': 'kits',
            'price': 2500.00,
            'stock': 30,
        },
    ]

    created_count = 0
    updated_count = 0

    for product_data in products_data:
        category = categories.get(product_data['category_slug'])
        if not category:
            print(f"❌ Категория не найдена: {product_data['category_slug']}")
            continue

        product, created = Product.objects.update_or_create(
            slug=product_data['slug'],
            defaults={
                'name': product_data['name'],
                'category': category,
                'description': product_data['description'],
                'price': product_data['price'],
                'stock': product_data['stock'],
                'is_active': True,
            }
        )

        if created:
            created_count += 1
            print(f"✅ Создан: {product.name}")
        else:
            updated_count += 1
            print(f"🔄 Обновлен: {product.name}")

    return created_count, updated_count


def check_database():
    """Проверяет состояние базы данных"""
    print("\n📊 ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("-" * 40)

    categories_count = Category.objects.count()
    products_count = Product.objects.count()

    print(f"📁 Категорий: {categories_count}")
    print(f"🛒 Продуктов: {products_count}")

    if products_count > 0:
        print("\n📋 Список продуктов:")
        for product in Product.objects.all()[:5]:
            print(f"  • {product.name} ({product.category.name}) - {product.price} руб.")
        if products_count > 5:
            print(f"  ... и еще {products_count - 5} продуктов")


def main():
    """Основная функция"""
    print("=" * 70)
    print("🚀 ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ПРОДУКТАМИ")
    print("=" * 70)

    try:
        # Создаем категории
        categories = create_categories()

        # Создаем продукты
        created, updated = create_products(categories)

        # Проверяем базу
        check_database()

        # Итоги
        print("\n" + "=" * 70)
        print("🎉 ИТОГИ:")
        print("=" * 70)
        print(f"✅ Создано новых продуктов: {created}")
        print(f"🔄 Обновлено продуктов: {updated}")
        print(f"📁 Всего категорий: {Category.objects.count()}")
        print(f"🛒 Всего продуктов: {Product.objects.count()}")

        print("\n🔗 Админка: http://127.0.0.1:8000/admin/")
        print("   Логин: admin / ваш_пароль")

        print("\n📝 Для просмотра в браузере:")
        print("   python manage.py runserver")
        print("   http://127.0.0.1:8000/")

    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        print("\n⚠️  Сначала создайте миграции:")
        print("   python manage.py makemigrations products")
        print("   python manage.py migrate")


if __name__ == "__main__":
    main()