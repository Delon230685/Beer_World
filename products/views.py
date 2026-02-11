from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets

from .models import Category, Product
from .serializers import ProductSerializer


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_active=True)[:5]
        context['is_home_page'] = True
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'  # 👈 ИЗМЕНИТЬ С 'base.html'!
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search')
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search')
        context['is_products_page'] = True
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'  # 👈 Это правильно!
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем похожие товары из той же категории
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context


class GuidesRecipesView(TemplateView):
    template_name = 'guides-recipes.html'


class ProductViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для просмотра и поиска товаров.
    """
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True).select_related('category')