from django_filters import rest_framework as filters
from .models import Product
from .custom_filter_backends import backends


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    name = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', 'name', 'freeDelivery']
