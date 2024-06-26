from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели User.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ['username', 'password']


class AuthUserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для логина пользователя.
    """
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели Profile.
    """
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
        fields = ['fullName', 'email', 'phone', 'avatar']


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для изменения данных пользователя.
    """

    def validate_phone(self, value):
        if len(value) != 10:
            raise serializers.ValidationError('Номер должен состоять из 10 цифр')
        return value

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone']
        extra_kwargs = {
            'email': {'validators': [EmailValidator, ]},
            'phone': {'validators': []},
        }


class UpdatePasswordSerializer(serializers.ModelSerializer):
    """
    Сериазайзер для изменения пароля пользователя.
    """

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['password']
