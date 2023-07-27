from datetime import datetime, timedelta
from rest_framework import status, mixins
from rest_framework.utils import json
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.schemas import DefaultSchema
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Category, Product, Review, Tag, CartList
from .paginations import CatalogPagination
from .filters import ProductFilter
from .cart import Cart
from .serializers import (
    CategoriesSerializer,
    ProductSerializer, CatalogSerializer,
    ReviewSerializer, CreateReviewSerializer,
    TagSerializer,
    SaleSerializer,
    CartSerializer,
)


@extend_schema(tags=['catalog'])
class CategoriesViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = None

    def get(self, request: Request) -> Response:
        return self.list(request)


class CatalogViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CatalogPagination
    filterset_class = ProductFilter

    def get(self, request: Request) -> Response:
        return self.list(request)


@extend_schema(tags=['catalog'], description='get catalog popular items')
class PopularProducts(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.order_by('-rating')[:4]
    serializer_class = CatalogSerializer
    pagination_class = None
    filterset_class = None


@extend_schema(tags=['catalog'], description='get catalog limited items')
class LimitedProducts(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.order_by('count')[:4]
    serializer_class = CatalogSerializer
    pagination_class = None
    filterset_class = None


@extend_schema(tags=['catalog'], description='get banner items')
class Banners(mixins.ListModelMixin, GenericViewSet):
    serializer_class = CatalogSerializer
    pagination_class = None
    filterset_class = None

    def get_queryset(self):
        categories = Category.objects.all()
        products = [Product.objects.filter(category=category).order_by('-rating')[:1] for category in categories]
        products = sorted(products, key=lambda item: item.values('rating')[0]['rating'], reverse=True)
        products_id = [item.values('id')[0]['id'] for item in products]
        return Product.objects.filter(id__in=products_id).order_by('-rating')[:4]


class Sale(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SaleSerializer
    pagination_class = CatalogPagination
    queryset = Product.objects.filter(sale__isnull=False, sale__date_to__gte=datetime.now() + timedelta(hours=3))


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddReview(ModelViewSet):
    queryset = Review.objects.prefetch_related('product')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    schema = DefaultSchema()

    def create(self, request: Request, pk: int) -> Response:
        print(request.data)
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=serializer.data, user=request.user, product_id=pk)
        return Response({'message': 'ok', 'review': serializer.data}, status=status.HTTP_200_OK)


class GetTags(GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request: Request) -> Response:
        print('GetTags request.data:', request.data)
        # products = Product.objects.filter(category__id=request.data.get('category'))
        # products = Product.objects.filter(category__id=1)
        products = Product.objects.all()
        tags = Tag.objects.filter(product__in=products).distinct()
        print('tags: ', tags)
        return Response(TagSerializer(tags, many=True).data)


class GetBasket(GenericAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        cart = Cart(self.request)
        return CartList.objects.filter(cart=cart.cart).order_by('product_id')

    def get(self, request):
        return Response(CartSerializer(self.get_queryset(), many=True).data)

    def post(self, request):
        cart = Cart(request)
        product = Product.objects.get(id=request.data.get('id'))
        count = request.data.get('count')
        cart.add(product=product, quantity=count)
        cart_list = CartList.objects.filter(cart=cart.cart).order_by('product_id')
        # products = Product.objects.filter(id__in=[item.product.id for item in cart_list])
        return Response(CartSerializer(cart_list, many=True).data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        data = json.loads(request.body.decode('utf-8'))
        cart = Cart(request)
        product = Product.objects.get(id=data.get('id'))
        count = data.get('count')
        cart.add(product=product, quantity=-count)
        cart_list = CartList.objects.filter(cart=cart.cart).order_by('product_id')
        # products = Product.objects.filter(id__in=[item.product.id for item in cart_list])
        return Response(CartSerializer(cart_list, many=True).data, status=status.HTTP_200_OK)
