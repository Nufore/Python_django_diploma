from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .cart import Cart
from .models import Profile, UserCart, CartList, Product
from .profile_serializers import (
    UserSerializer,
    AuthUserSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    UpdatePasswordSerializer,
    RegisterSerializer,
)


class SignIn(GenericAPIView):
    serializer_class = AuthUserSerializer

    @extend_schema(tags=['auth'], description='sign in')
    def post(self, request: Request) -> Response:
        data = json.loads(list(request.data.keys())[0])
        user = get_object_or_404(User, username=data['username'])
        if not user.check_password(data['password']):
            Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return Response({'detail': 'success', 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'bad credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUp(GenericAPIView):
    serializer_class = UserSerializer

    @extend_schema(tags=['auth'], description='sign up')
    def post(self, request: Request) -> Response:
        data = json.loads(list(request.data.keys())[0])
        serializer = RegisterSerializer(data=data)
        anon_cart = Cart(request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=data['username'])
            user.set_password(data['password'])
            user.save()
            profile = Profile.objects.create(user=user, fullName=data['name'])
            profile.save()

            if anon_cart.cart:
                cart = UserCart.objects.create(user=user)
                for item in anon_cart:
                    CartList.objects.create(cart=cart,
                                            product=Product.objects.get(id=int(item['product'].id)),
                                            count=int(item['quantity']))
                anon_cart.clear()

            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'not ok'}, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], description='sign out')
@ensure_csrf_cookie
@api_view(['POST'])
def sign_out(request: Request) -> Response:
    logout(request)
    return Response({'detail': 'successful logout'}, status=status.HTTP_200_OK)


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data)

    def post(self, request: Request) -> Response:
        profile = get_object_or_404(Profile, user=request.user)
        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=profile, validated_data=serializer.data)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileUpdatePassword(GenericAPIView):
    serializer_class = UpdatePasswordSerializer

    def post(self, request: Request) -> Response:
        user = User.objects.get(id=request.user.id)
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.data)
        return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)


class ProfileUpdateAvatar(APIView):

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.avatar = request.FILES['avatar']
        profile.save()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
