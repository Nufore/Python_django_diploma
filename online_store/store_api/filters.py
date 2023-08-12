from django_filters import rest_framework as filters
from .models import Product, Tag


class ProductFilter(filters.FilterSet):
    """
    Фильтр товаров
    """
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    name = filters.CharFilter(field_name="title", lookup_expr='icontains')
    available = filters.BooleanFilter(field_name='count', lookup_expr='gte')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all())
    sort = filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('date', 'date'),
            ('rating', 'rating'),
            ('reviews', 'reviews'),
        ),
    )

    class Meta:
        model = Product
        fields = ['price', 'name', 'freeDelivery']
