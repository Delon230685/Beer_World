import pytest
from rest_framework.test import APIClient
from .models import Category, Product


@pytest.mark.django_db
class TestProductAPI:
    def test_get_products_list(self):
        client = APIClient()
        # Создаем тестовые данные
        cat = Category.objects.create(name="Hops", slug="hops")
        Product.objects.create(name="Citra", slug="citra", price=100, category=cat, stock=10, is_active=True)

        response = client.get('/api/products/')

        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == "Citra"
