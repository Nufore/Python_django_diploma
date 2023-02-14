from django.urls import path
from .views import ProductDetailView, ProductListView, base


urlpatterns = [
    path('base/', base, name='base'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
