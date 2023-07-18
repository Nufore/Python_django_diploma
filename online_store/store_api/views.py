from rest_framework import status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.schemas import DefaultSchema
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, Review, Tag
from .paginations import CatalogPagination
from .filters import ProductFilter
from .serializers import (
    CategoriesSerializer,
    ProductSerializer, CatalogSerializer,
    ReviewSerializer, CreateReviewSerializer,
    TagSerializer
)


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
