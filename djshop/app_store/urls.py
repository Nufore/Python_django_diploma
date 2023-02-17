from django.urls import path
from .views import ProductDetailView, ProductListView, base, DynamicReviewLoad


urlpatterns = [
    path('base/', base, name='base'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('load-more-reviews/', DynamicReviewLoad.as_view(), name='load-more-reviews')
]
