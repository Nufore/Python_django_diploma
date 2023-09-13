from datetime import datetime, timedelta
from django.db.models import Sum, Count
from rest_framework import serializers
from .models import Category, Product, Review, ProductImages, Tag, ProductSpecifications, CartList, Order, OrderList


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer для категорий товаров.
    """
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


class CreateReviewSerializer(serializers.ModelSerializer):
    """
    Serializer для создания отзыва о товаре.
    """
    def create(self, validated_data, user, product_id):
        product = Product.objects.get(id=product_id)
        review = Review.objects.create(
            user=user,
            product=product,
            author=validated_data['author'],
            email=validated_data['email'],
            text=validated_data['text'],
            rate=validated_data['rate']
        )
        review.save()
        product.update_rating()
        return review

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer для отзыва о товаре.
    """
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        date = obj.date.strftime("%Y-%m-%d %H:%m")
        return date

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    """
    Serializer спецификации товара.
    """
    class Meta:
        model = ProductSpecifications
        fields = ['name', 'value']


class ProductImagesSerializer(serializers.ModelSerializer):
    """
    Serializer для модели ProductImages.
    """
    # image = serializers.SerializerMethodField()
    src = serializers.CharField(source='image.url')
    # alt = serializers.CharField()
    #
    # def get_image(self, obj):
    #     return {
    #         'src': obj.image.url,
    #         'alt': 'Image alt string'
    #     }

    class Meta:
        model = ProductImages
        fields = ['src']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer модели Product.
    """
    date = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date.strftime("%a %b %d %Y %H:%M:%S %Z%z")

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj)
        return ReviewSerializer(reviews, many=True).data

    def get_images(self, obj):
        images = ProductImages.objects.filter(product=obj)
        return ProductImagesSerializer(images, many=True).data

    def get_tags(self, obj):
        tags = Tag.objects.filter(product=obj)
        return TagSerializer(tags, many=True).data

    def get_specifications(self, obj):
        specifications = ProductSpecifications.objects.filter(product=obj)
        return ProductSpecificationsSerializer(specifications, many=True).data

    def get_price(self, obj):
        if obj.sale and obj.sale.date_to >= datetime.now() + timedelta(hours=3):
            return obj.price - obj.sale.discount
        else:
            return obj.price

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            'specifications',
            'reviews',
            'rating',
        ]


class CatalogSerializer(ProductSerializer):
    """
    Измененный ProductSerializer для отображения количества отзывов о товаре.
    """

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj).aggregate(Count('id'))
        return reviews['id__count']


class CartSessionSerializer(serializers.Serializer):
    """
    Serializer для корзины неавторизованного пользователя.
    """
    id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    # price = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.SerializerMethodField()
    count = serializers.IntegerField(source='quantity')
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_price(self, obj):
        if obj['product'].sale and obj['product'].sale.date_to >= datetime.now() + timedelta(hours=3):
            return obj['product'].price - obj['product'].sale.discount
        else:
            return obj['product'].price

    def get_id(self, obj):
        return obj['product'].id

    def get_category(self, obj):
        return obj['product'].category.id

    def get_date(self, obj):
        return obj['product'].date.strftime("%a %b %d %Y %H:%M:%S %Z%z")

    def get_title(self, obj):
        return obj['product'].title

    def get_description(self, obj):
        return obj['product'].description

    def get_freeDelivery(self, obj):
        return obj['product'].freeDelivery

    def get_images(self, obj):
        images = ProductImages.objects.filter(product=obj['product'])
        return ProductImagesSerializer(images, many=True).data

    def get_tags(self, obj):
        tags = Tag.objects.filter(product=obj['product'])
        return TagSerializer(tags, many=True).data

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj['product']).aggregate(Count('id'))
        return reviews['id__count']

    def get_rating(self, obj):
        return obj['product'].rating


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer корзины авторизованного пользователя.
    """
    id = serializers.IntegerField(source='product.id')
    category = serializers.IntegerField(source='product.category.id')
    # price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    price = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.CharField(source='product.title')
    description = serializers.CharField(source='product.description')
    freeDelivery = serializers.CharField(source='product.freeDelivery')
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.CharField(source='product.rating')

    def get_price(self, obj):
        if obj.product.sale and obj.product.sale.date_to >= datetime.now() + timedelta(hours=3):
            return obj.product.price - obj.product.sale.discount
        else:
            return obj.product.price

    def get_date(self, obj):
        return obj.product.date.strftime("%a %b %d %Y %H:%M:%S %Z%z")

    def get_images(self, obj):
        images = ProductImages.objects.filter(product=obj.product)
        return ProductImagesSerializer(images, many=True).data

    def get_tags(self, obj):
        tags = Tag.objects.filter(product=obj.product)
        return TagSerializer(tags, many=True).data

    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj.product).aggregate(Count('id'))
        return reviews['id__count']

    class Meta:
        model = CartList
        fields = [
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            # 'fullDescription',
            'freeDelivery',
            'images',
            'tags',
            # 'specifications',
            'reviews',
            'rating',
        ]


class SaleSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения товаров со скидками.
    """
    salePrice = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_salePrice(self, obj):
        return obj.price - obj.sale.discount

    def get_dateFrom(self, obj):
        return obj.sale.date_from.strftime("%Y-%m-%d")

    def get_dateTo(self, obj):
        return obj.sale.date_to.strftime("%Y-%m-%d")

    def get_images(self, obj):
        images = ProductImages.objects.filter(product=obj)
        return ProductImagesSerializer(images, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']


class GetOrderSerializer(serializers.ModelSerializer):
    """
    Сериазайзер для заказа.
    """
    createdAt = serializers.SerializerMethodField()
    fullName = serializers.CharField(source='user.profile.fullName')
    email = serializers.CharField(source='user.profile.email')
    phone = serializers.CharField(source='user.profile.phone')
    deliveryType = serializers.CharField(source='delivery.type.name')
    paymentType = serializers.CharField(source='payment.type.name')
    totalCost = serializers.FloatField(source='total_cost')
    status = serializers.CharField(source='payment.status.name')
    city = serializers.CharField(source='delivery.city')
    address = serializers.CharField(source='delivery.address')
    products = serializers.SerializerMethodField()
    paymentError = serializers.CharField(source='payment.error_message')

    def get_products(self, obj):
        items = OrderList.objects.filter(order=obj)
        return CartSerializer(items, many=True).data

    def get_createdAt(self, obj):
        return obj.order_date.strftime("%Y-%m-%d %H:%M")

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
            'paymentError',
        ]
