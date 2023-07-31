from django.core.management import BaseCommand
from store_api.models import Product, Review, ProductImages, Tag
from django.db.models import Sum, Count
from store_api.serializers import TagSerializer, ProductImagesSerializer
from datetime import datetime, timedelta
from rest_framework import serializers


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo agg')
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=3)

        cart = [
            {'quantity': 1, 'price': '500.00', 'product': product1, 'total_price': '500.00'},
            {'quantity': 3, 'price': '1500.00', 'product': product2, 'total_price': '4500.00'}
        ]

        cart_data = [{'id': item['product'].id, 'count': item['quantity']} for item in cart]
        print('cart_data: ', cart_data)

        class TestSerializer(serializers.Serializer):
            quantity = serializers.IntegerField()
            price = serializers.DecimalField(max_digits=10, decimal_places=2)
            product = serializers.IntegerField()
            total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

        # serializer = TestSerializer(cart, many=True)
        # print('DATA: ', dict(serializer.data[0])['product'])

        cart_2 = [
            {'product': 1, 'quantity': 3},
            {'product': 3, 'quantity': 5},
        ]

        class CartSessionSerializer(serializers.Serializer):
            id = serializers.SerializerMethodField()
            category = serializers.SerializerMethodField()
            price = serializers.DecimalField(max_digits=10, decimal_places=2)
            count = serializers.IntegerField(source='quantity')
            date = serializers.SerializerMethodField()
            title = serializers.SerializerMethodField()
            description = serializers.SerializerMethodField()
            freeDelivery = serializers.SerializerMethodField()
            images = serializers.SerializerMethodField()
            tags = serializers.SerializerMethodField()
            reviews = serializers.SerializerMethodField()
            rating = serializers.SerializerMethodField()

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

        class TestSerializerTwo(serializers.Serializer):
            id = serializers.SerializerMethodField()
            count = serializers.IntegerField(source='quantity')
            price = serializers.SerializerMethodField()

            def get_id(self, obj):
                return obj['product'].id

            def get_price(self, obj):
                return obj['product'].price

        serializer2 = TestSerializerTwo(cart, many=True)
        print('DATA2: ', dict(serializer2.data[0]))

        serializer3 = CartSessionSerializer(cart, many=True)
        print('DATA3: ', serializer3.data)

        self.stdout.write('Done')
