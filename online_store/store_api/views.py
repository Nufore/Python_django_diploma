from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import GenericViewSet, ModelViewSet

from rest_framework.generics import GenericAPIView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from .models import ProductCategory, Product
from .serializers import CategoriesSerializer, UserSerializer, AuthUserSerializer, ProductSerializer

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, extend_schema_field


class CategoriesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request: Request) ->Response:
        return self.list(request)


class ProductViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AuthApiView(GenericAPIView):
    serializer_class = AuthUserSerializer

    @extend_schema(
        tags=['auth'],
        description='sign in',
    )
    def post(self, request: Request) -> Response:
        print(request.POST)
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            login(request, user)
            return Response({'token': token.key, 'user': serializer.data})
        else:
            return Response({'detail': 'bad credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    tags=['auth'],
    description='sign in',
    parameters=[
        OpenApiParameter(
            name='username',
            description='username',
            required=True,
            type=str
        ),
        OpenApiParameter(
            name='password',
            description='password',
            required=True,
            type=str
        ),
    ],
)
@api_view(['POST'])
def sign_in(request: Request) -> Response:
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        login(request, user)
        return Response({'token': token.key, 'user': serializer.data})
    else:
        return Response({'detail': 'bad credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    tags=['auth'],
    description='sign up',
)
@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key,
                         'user': serializer.data})
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], description='sign out')
@api_view(['POST'])
def sign_out(request: Request) -> Response:
    user = get_object_or_404(User, username=request.data['username'])
    if user:
        logout(request)
        return Response({'detail': 'successful logout'}, status=status.HTTP_200_OK)
