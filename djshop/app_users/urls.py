from django.urls import path
from .views import register_view, Account, UserLoginView, UserLogoutView, UserEditView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('account/', Account.as_view(), name='account'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserEditView.as_view(), name='profile'),
]
