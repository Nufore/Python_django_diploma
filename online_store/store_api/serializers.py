from django.contrib.auth.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .models import Category, Product, Feedback


class CategoriesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': 'Image alt string'
        }

    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent=obj.id)
        return CategoriesSerializer(subcategories, many=True).data

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'product', 'text', 'rate', 'added_at']


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = Feedback.objects.filter(product=obj)
        return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'added_at', 'name', 'description', 'picture', 'reviews']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
