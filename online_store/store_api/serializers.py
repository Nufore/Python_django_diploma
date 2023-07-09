from rest_framework import serializers
from .models import Category, Product, Review, ProductImages, Tag, ProductSpecifications


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


class CreateReviewSerializer(serializers.ModelSerializer):
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
        return review

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date']


class ReviewSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = ProductSpecifications
        fields = ['name', 'value']


class ProductImagesSerializer(serializers.ModelSerializer):
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
    date = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()

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
            'reviews',
            'specifications',
        ]
