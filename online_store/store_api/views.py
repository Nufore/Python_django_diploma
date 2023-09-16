import time
from datetime import datetime, timedelta
from rest_framework import status, mixins
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.schemas import DefaultSchema
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db.models import Sum, F

from .models import Category, Product, Review, Tag, UserCart, CartList, Order, OrderList, Delivery, DeliveryType, \
    PaymentType, Payment, PaymentStatus
from .paginations import CatalogPagination
from .filters import ProductFilter
from .cart import Cart
from .serializers import (
    CategoriesSerializer,
    ProductSerializer, CatalogSerializer,
    ReviewSerializer, CreateReviewSerializer,
    TagSerializer,
    SaleSerializer,
    CartSerializer, CartSessionSerializer,
    GetOrderSerializer,
)


@extend_schema(tags=['catalog'])
class CategoriesViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    Вью для отображения категорий товаров.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = None

    def get(self, request: Request) -> Response:
        return self.list(request)


class CatalogViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    Вью для отображения товаров.
    """
    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CatalogPagination
    filterset_class = ProductFilter

    def get(self, request: Request) -> Response:
        return self.list(request)


@extend_schema(tags=['catalog'], description='get catalog popular items')
class PopularProducts(mixins.ListModelMixin, GenericViewSet):
    """
    Вью для отображения на главной странице товаров в разделе POPULAR PRODUCTS
    """
    queryset = Product.objects.order_by('-rating')[:4]
    serializer_class = CatalogSerializer
    pagination_class = None
    filterset_class = None


@extend_schema(tags=['catalog'], description='get catalog limited items')
class LimitedProducts(mixins.ListModelMixin, GenericViewSet):
    """
    Вью для отображения на главной странице товаров в разделе LIMITED EDITION
    """
    queryset = Product.objects.order_by('count')[:4]
    serializer_class = CatalogSerializer
    pagination_class = None
    filterset_class = None


@extend_schema(tags=['catalog'], description='get banner items')
class Banners(mixins.ListModelMixin, GenericViewSet):
    """
    Вью для отображения на главной странице товаров Banners
    """
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
    """
    Вью для отображения товаров на странице sale
    """
    serializer_class = SaleSerializer
    pagination_class = CatalogPagination
    queryset = Product.objects.filter(sale__isnull=False, sale__date_to__gte=datetime.now() + timedelta(hours=3))


class ProductViewSet(ModelViewSet):
    """
    Вью для отображения данных товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddReview(ModelViewSet):
    """
    Добавление отзыва к товару.
    """
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
    """
    Получение тэгов товаров.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request: Request) -> Response:
        products = Product.objects.all()
        tags = Tag.objects.filter(product__in=products).distinct()
        return Response(TagSerializer(tags, many=True).data)


class Basket(GenericAPIView):
    """
    Вью для отображения корзины, добавления и удаления товара.
    """
    # serializer_class = CartSerializer

    def get_serializer_class(self):
        cart = Cart(self.request)
        if cart.is_model_cart():
            return CartSerializer
        else:
            return CartSessionSerializer

    def get_queryset(self):
        cart = Cart(self.request)
        if cart.is_model_cart():
            return CartList.objects.filter(cart=cart.cart).order_by('product_id')
        else:
            return None

    def get(self, request):
        cart = Cart(request)
        if cart.is_model_cart():
            return Response(CartSerializer(self.get_queryset(), many=True).data)
        else:
            return Response(
                CartSessionSerializer(cart.get_cart_for_serializer(), many=True).data,
                status=status.HTTP_200_OK
            )

    def post(self, request):
        cart = Cart(request)
        product = Product.objects.get(id=request.data.get('id'))
        count = request.data.get('count')
        cart.add(product=product, quantity=count)
        if cart.is_model_cart():
            cart_list = CartList.objects.filter(cart=cart.cart).order_by('product_id')
            return Response(CartSerializer(cart_list, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(
                CartSessionSerializer(cart.get_cart_for_serializer(), many=True).data,
                status=status.HTTP_200_OK
            )

    def delete(self, request: Request) -> Response:
        data = json.loads(request.body.decode('utf-8'))
        cart = Cart(request)
        product = Product.objects.get(id=data.get('id'))
        count = data.get('count')
        cart.add(product=product, quantity=-count)
        if cart.is_model_cart():
            cart_list = CartList.objects.filter(cart=cart.cart).order_by('product_id')
            return Response(CartSerializer(cart_list, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(
                CartSessionSerializer(cart.get_cart_for_serializer(), many=True).data,
                status=status.HTTP_200_OK
            )


class CreateOrder(GenericAPIView):
    """
    Создание заказа.
    """
    serializer_class = CartSerializer

    def get_queryset(self):
        cart = Cart(self.request)
        if cart.is_model_cart():
            return CartList.objects.filter(cart=cart.cart).order_by('product_id')
        else:
            return None

    def post(self, request):
        cart = Cart(request)
        if cart.is_model_cart():
            cart_list = CartList.objects.select_related('product').filter(cart=cart.cart)
            cart_summ = CartList.objects.filter(cart=cart.cart).aggregate(total=Sum(F('product__price') * F('count')))
            discount_summ = CartList.objects.filter(cart=cart.cart).aggregate(
                total=Sum(F('product__sale__discount') * F('count'))
            )
            if discount_summ['total'] is not None:
                cart_summ['total'] -= discount_summ['total']

            delivery_type = DeliveryType.objects.get(id=1)
            default_delivery = Delivery.objects.create(type=delivery_type, city='', address='')
            payment_type = PaymentType.objects.get(id=1)
            payment_status = PaymentStatus.objects.get(id=1)
            default_payment = Payment.objects.create(type=payment_type, status=payment_status)

            new_order = Order.objects.create(
                user=request.user,
                total_cost=float(cart_summ['total']),
                delivery=default_delivery,
                payment=default_payment,
            )
            for item in cart_list:
                OrderList.objects.create(order=new_order, product=item.product, count=item.count)
            cart.cart.delete()
            return Response({"orderId": new_order.id})
        else:
            new_order = Order.objects.last()
            return Response({"orderId": new_order.id + 1})

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(GetOrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)


class GetOrder(APIView):
    """
    Вью для направления на оплату заказа
    """
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        return Response(GetOrderSerializer(order).data)

    def post(self, request, pk):
        order = Order.objects.get(id=int(pk))
        order.delivery.city = request.data.get('city')
        order.delivery.address = request.data.get('address')
        order.delivery.save()
        order.payment.status = PaymentStatus.objects.get(id=2)
        order.payment.save()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    """
    Оплата заказа.
    """
    def post(self, request, pk):
        order = Order.objects.get(id=int(pk))
        order.payment.card_number = request.data.get('number')
        order.payment.error_message = None
        order.payment.save()
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class GetPaymentResponse(APIView):
    """
    Проверка статуса заказа.
    Если 'paid' то True
    """
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        time.sleep(5)
        if order.payment.status.id == 3:
            return Response({'data': True})
        else:
            return Response({'data': False})
