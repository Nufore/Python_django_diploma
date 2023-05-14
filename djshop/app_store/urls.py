from django.urls import path
from .views import ProductDetailView, ProductListView, base, DynamicReviewLoad, CartView, product_list,\
    product_detail, OrderDeliveryView, OrderDetailView, PaymentView, progress_payment, OrderListView, \
    GetPaymentResponse, HistoryOrderView, base_add_product


urlpatterns = [
    path('base/', base, name='base'),
    path('add/<int:product_id>/<str:url_redirect>/', base_add_product, name='add_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('load-more-reviews/', DynamicReviewLoad.as_view(), name='load-more-reviews'),
    path('cart/', CartView.as_view(), name='cart'),
    path('order/', OrderDeliveryView.as_view(), name='order'),
    path('order-detail/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('payment/<int:pk>', PaymentView.as_view(), name='payment'),
    path('progress-payment/<int:pk>', progress_payment, name='progress-payment'),
    path('get-payment-response/<int:pk>', GetPaymentResponse.as_view(), name='get-payment-response'),
    path('history-order/', HistoryOrderView.as_view(), name='history-order'),

    path('new_product_list', product_list, name='new_product_list'),
    path('new_product_detail/<int:id>', product_detail, name='new_product_detail'),
]
