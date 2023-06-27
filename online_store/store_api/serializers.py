from .models import ProductCategory, Product
from django.contrib.auth.models import User
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'added_at', 'name', 'description', 'picture']


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['username', 'password']
