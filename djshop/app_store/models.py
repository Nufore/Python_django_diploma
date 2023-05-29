from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, null=False, on_delete=models.CASCADE)
    picture = models.ImageField(default=None, null=True, upload_to='product_pictures/', blank=True)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    feedback_count = models.IntegerField(default=0, null=False)
    added_at = models.DateTimeField(auto_now_add=True)
    manufacturer = models.CharField(max_length=200)
    limited_edition = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_store:new_product_detail', args=[self.id])


class ProductPictures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(default=None, null=True, upload_to='product_pictures/')


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    rate = models.IntegerField(null=True, default=None)
    added_at = models.DateTimeField(auto_now_add=True)


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


class PaymentStatus(models.Model):
    name = models.CharField(max_length=20)


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


class Delivery(models.Model):
    type = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField(default=0.0, null=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)


class OrderList(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
