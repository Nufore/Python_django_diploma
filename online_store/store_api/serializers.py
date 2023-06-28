from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import serializers

from .models import ProductCategory, Product, Feedback


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'product', 'text', 'rate', 'added_at']


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = get_list_or_404(Feedback, product=obj)
        return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'added_at', 'name', 'description', 'picture', 'reviews']


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['username', 'password']
