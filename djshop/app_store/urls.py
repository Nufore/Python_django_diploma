from django.urls import path
from .views import ProductDetailView, ProductListView, base, DynamicReviewLoad, CartView, product_list,\
    product_detail, OrderDeliveryView


urlpatterns = [
    path('base/', base, name='base'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('load-more-reviews/', DynamicReviewLoad.as_view(), name='load-more-reviews'),
    path('cart/', CartView.as_view(), name='cart'),
    path('order/', OrderDeliveryView.as_view(), name='order'),

    path('new_product_list', product_list, name='new_product_list'),
    path('new_product_detail/<int:id>', product_detail, name='new_product_detail'),
]
