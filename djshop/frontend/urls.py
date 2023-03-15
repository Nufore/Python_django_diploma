from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="frontend/index.html")),
    path('about/', TemplateView.as_view(template_name="frontend/about.html")),
    path('account/', TemplateView.as_view(template_name="frontend/account.html")),  # TODO получать данные в шаблон
    path('cart/', TemplateView.as_view(template_name="frontend/cart.html")),
    path('catalog/', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('catalog/<int:pk>', TemplateView.as_view(template_name="frontend/catalog.html")),
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),  # TODO получать данные в шаблон
    path('order-detail/<int:pk>', TemplateView.as_view(template_name="frontend/oneorder.html")),  # TODO получать данные в шаблон
    path('order/', TemplateView.as_view(template_name="frontend/order.html")),
    path('payment/', TemplateView.as_view(template_name="frontend/payment.html")),  # TODO реализовать отправку формы оплаты
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html")),  # TODO реализовать отправку формы оплаты
    path('product/<int:pk>', TemplateView.as_view(template_name="frontend/product.html")),
    path('profile/', TemplateView.as_view(template_name="frontend/profile.html")),  # TODO получать данные в шаблон
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html")),
    path('sale/', TemplateView.as_view(template_name="frontend/sale.html")),
]
