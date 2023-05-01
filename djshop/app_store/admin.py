from django.contrib import admin
from .models import ProductCategory, Product, ProductPictures, Feedback, UserCart, CartList, Delivery, PaymentType, \
    PaymentStatus, DeliveryType, Order, OrderList


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price']


class ProductPicturesAdmin(admin.ModelAdmin):
    list_display = ['product', 'id']


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'added_at']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user']


class CartListAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'count']


class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_express', 'express_price', 'base_less_than', 'base_price']


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'city', 'address']


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_cost', 'payment', 'delivery']


class OrderListAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'count']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPictures, ProductPicturesAdmin)
admin.site.register(Feedback, FeedBackAdmin)
admin.site.register(UserCart, CartAdmin)
admin.site.register(CartList, CartListAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(PaymentStatus, PaymentStatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderList, OrderListAdmin)
