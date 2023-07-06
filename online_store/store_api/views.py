from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.schemas import DefaultSchema
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Category, Product, Review, Profile
from .serializers import (
    CategoriesSerializer,
    UserSerializer,
    AuthUserSerializer,
    ProductSerializer,
    ReviewSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    UserUpdatePasswordSerializer,
    UpdateAvatarSerializer,
    RegisterSerializer
)


class CategoriesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = None

    def get(self, request: Request) -> Response:
        return self.list(request)


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


class UserUpdatePassword(GenericAPIView):
    serializer_class = UserUpdatePasswordSerializer

    def post(self, request: Request) -> Response:
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(request.data['password'])
        user.save()
        logout(request)
        return Response({'message': 'password changed successfully'}, status=status.HTTP_200_OK)


class ProfileUpdateAvatar(GenericAPIView):
    serializer_class = UpdateAvatarSerializer

    def post(self, request):
        print(request.FILES['avatar'])
        print(request.data)
        serializer = UpdateAvatarSerializer(data=request.FILES)
        profile = get_object_or_404(Profile, user=request.user)
        serializer.is_valid(raise_exception=True)
        profile.avatar = request.FILES['avatar']
        profile.save()
        return Response(UpdateAvatarSerializer(profile).data, status=status.HTTP_200_OK)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddReview(ModelViewSet):
    queryset = Review.objects.prefetch_related('product')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    schema = DefaultSchema()

    def create(self, request: Request, pk:int) -> Response:
        print(request.data)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'ok', 'review': serializer.data}, status=status.HTTP_200_OK)


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
        print(data)
        # serializer = RegisterSerializer(data=data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     user = User.objects.get(username=data['username'])
        #     user.set_password(data['password'])
        #     user.save()
        #     return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'not ok'}, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], description='sign out')
@ensure_csrf_cookie
@api_view(['POST'])
def sign_out(request: Request) -> Response:
    logout(request)
    return Response({'detail': 'successful logout'}, status=status.HTTP_200_OK)
