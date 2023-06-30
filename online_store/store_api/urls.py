from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoriesViewSet,
    sign_out,
    SignIn,
    SignUp,
    ProductViewSet,
    AddReview,
)


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('product', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('sign-in/', SignIn.as_view()),
    path('sign-up/', SignUp.as_view()),
    path('sign-out/', sign_out),
    path('product/<str:pk>/review/', AddReview.as_view({'post': 'create'})),
]
