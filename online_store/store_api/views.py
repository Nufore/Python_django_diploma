from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.schemas import AutoSchema, DefaultSchema

from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from .models import ProductCategory, Product, Feedback
from .serializers import CategoriesSerializer, UserSerializer, AuthUserSerializer, ProductSerializer, ReviewSerializer


class CategoriesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)


class ProductViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(description='get catalog item')
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class AddReview(ModelViewSet):
    queryset = Feedback.objects.prefetch_related('product')
    serializer_class = ReviewSerializer
    schema = DefaultSchema()

    def create(self, request: Request, pk:int) -> Response:
        product = Product.objects.get(id=pk)
        user = User.objects.get(id=request.data['user'])
        text = request.data['text']
        rate = request.data['rate']
        review = Feedback.objects.create(product=product, user=user, text=text, rate=rate)
        review.save()
        return Response({'message': 'ok', 'review': ReviewSerializer(review).data}, status=status.HTTP_200_OK)


class SignIn(GenericAPIView):
    serializer_class = AuthUserSerializer

    @extend_schema(tags=['auth'], description='sign in')
    def post(self, request: Request) -> Response:
        print(request.POST)
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            login(request, user)
            return Response({'detail': 'success', 'user': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'bad credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUp(GenericAPIView):
    serializer_class = UserSerializer

    @extend_schema(tags=['auth'], description='sign up')
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'], description='sign out')
@api_view(['POST'])
def sign_out(request: Request) -> Response:
    logout(request)
    return Response({'detail': 'successful logout'}, status=status.HTTP_200_OK)
