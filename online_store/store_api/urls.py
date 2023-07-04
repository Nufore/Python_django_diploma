from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoriesViewSet,
    sign_out,
    SignIn,
    SignUp,
    ProductViewSet,
    AddReview,
    ProfileView,
    UserUpdatePassword,
    ProfileUpdateAvatar
)


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
# router.register('profile', ProfileView)


urlpatterns = [
    path('', include(router.urls)),
    path('sign-in/', SignIn.as_view()),
    path('sign-up/', SignUp.as_view()),
    path('sign-out/', sign_out),
    path('product/<str:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('product/<str:pk>/review/', AddReview.as_view({'post': 'create'})),
    path('profile/', ProfileView.as_view()),
    path('profile/password/', UserUpdatePassword.as_view()),
    path('profile/avatar/', ProfileUpdateAvatar.as_view())

]
