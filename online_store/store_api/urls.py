from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoriesViewSet,
    ProductViewSet,
    AddReview,
    CatalogViewSet,
    GetTags,
    PopularProducts, LimitedProducts, Banners,
    Sale,
    Basket,
    CreateOrder, GetOrder
)
from .profile_views import (sign_out, SignIn, SignUp, ProfileView, ProfileUpdatePassword, ProfileUpdateAvatar)


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('catalog', CatalogViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('sign-in/', SignIn.as_view()),
    path('sign-up', SignUp.as_view()),
    path('sign-out/', sign_out),
    path('product/<str:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('product/<str:pk>/review/', AddReview.as_view({'post': 'create'})),
    path('profile/', ProfileView.as_view()),
    path('profile/password/', ProfileUpdatePassword.as_view()),
    path('profile/avatar/', ProfileUpdateAvatar.as_view()),
    path('tags/', GetTags.as_view()),
    path('products/popular/', PopularProducts.as_view({'get': 'list'})),
    path('products/limited/', LimitedProducts.as_view({'get': 'list'})),
    path('banners/', Banners.as_view({'get': 'list'})),
    path('sales/', Sale.as_view({'get': 'list'})),
    path('basket/', Basket.as_view()),
    path('orders/', CreateOrder.as_view()),
    path('order/<str:pk>/', GetOrder.as_view())
]
