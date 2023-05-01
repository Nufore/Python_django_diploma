from django.urls import path
from .views import get_response


urlpatterns = [
    path('payment', get_response)
]
