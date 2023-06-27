from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoriesViewSet,
    sign_in,
    sign_up,
    sign_out,
    AuthApiView,
    ProductViewSet
)


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('product', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('sign-in/', sign_in),
    path('sign-up/', sign_up),
    path('sign-out/', sign_out),
    path('new_sign_in', AuthApiView.as_view()),
]
