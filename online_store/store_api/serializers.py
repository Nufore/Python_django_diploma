from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Category, Product, Review, Profile


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
        model = Review
        fields = ['id', 'user', 'product', 'text', 'rate', 'added_at']


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj)
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


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        if obj.avatar:
            return {
                'src': obj.avatar.url,
                'alt': 'Image alt string'
            }
        else:
            return None

    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'phone', 'avatar']


class UpdateProfileSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError('Номер должен состоять из 10 цифр')
        return value

    class Meta:
        model = Profile
        fields = ['fullname', 'email', 'phone']
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]},
            'phone': {'validators': []},
        }


class UserUpdatePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password']


class UpdateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']
