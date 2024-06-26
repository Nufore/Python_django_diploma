from django.db import models
from django.db.models import Sum, Count, QuerySet
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default=None, null=True, upload_to='product_categories/', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(default=None, null=True, upload_to='profile_avatars/', blank=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Sale(models.Model):
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    def __str__(self):
        return str(self.discount)


class Product(models.Model):
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    description = models.CharField(max_length=255)
    fullDescription = models.CharField(max_length=1000)
    freeDelivery = models.BooleanField(default=False)
    rating = models.DecimalField(null=True, default=None, blank=True, max_digits=3, decimal_places=2)
    reviews = models.IntegerField(default=0)
    sale = models.OneToOneField(Sale, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def update_rating(self):
        count_review = Review.objects.filter(product=self).aggregate(Count('id'))
        if count_review['id__count'] >= 1:
            sum_review_rate = Review.objects.filter(product=self).aggregate(Sum('rate'))
            self.rating = round(sum_review_rate['rate__sum'] / count_review['id__count'], 2)
            self.reviews = count_review['id__count']
            self.save()
            return self.rating
        else:
            return None


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(default=None, null=True, upload_to='product_images/')

    def __str__(self):
        return f'id={self.pk}, name={self.image.name}'.replace('product_images/', '')


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Specification'


class Review(models.Model):
    rate_choices = [
        (
            "RATE",
            [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]
        ),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=False, default=None)
    text = models.TextField(null=False)
    rate = models.IntegerField(null=True, default=None, choices=rate_choices)
    date = models.DateTimeField(auto_now_add=True)


class UserCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartList(models.Model):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


class PaymentType(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class PaymentStatus(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Payment(models.Model):
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    error_message = models.CharField(max_length=255, default=None, null=True)
    card_number = models.CharField(max_length=8, default=None, null=True)


class DeliveryType(models.Model):
    name = models.CharField(max_length=20)
    is_express = models.BooleanField(default=False)
    express_price = models.FloatField(default=500.0, null=True)
    base_less_than = models.FloatField(default=2000.0, null=True)
    base_price = models.FloatField(default=200, null=True)

    def __str__(self):
        return self.name


class Delivery(models.Model):
    type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField(default=0.0, null=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)


class OrderList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
