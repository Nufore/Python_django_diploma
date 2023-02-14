from django.db import models
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, null=False, on_delete=models.CASCADE)
    picture = models.ImageField(default=None, null=True, upload_to='product_pictures/')
    description = models.CharField(max_length=300)
    price = models.FloatField(default=0.0, null=False)
    feedback_count = models.IntegerField(default=0, null=False)
    added_at = models.DateTimeField(auto_now_add=True)
    manufacturer = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductPictures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(default=None, null=True, upload_to='product_pictures/')


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    added_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartList(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


class PaymentType(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=20)


class PaymentStatus(models.Model):
    name = models.CharField(max_length=20)


class Payment(models.Model):
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    error_message = models.CharField(max_length=255)
    card_number = models.CharField(max_length=8)


class Delivery(models.Model):
    name = models.CharField(max_length=20)
    is_express = models.BooleanField(default=False)
    express_price = models.FloatField(default=500.0, null=True)
    base_less_than = models.FloatField(default=2000.0, null=True)
    base_price = models.FloatField(default=200, null=True)


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField(default=0.0, null=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    delivery_type = models.ForeignKey(Delivery, on_delete=models.CASCADE)


class OrderList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
