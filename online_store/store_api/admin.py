from django.contrib import admin
from .models import Category, Product, Profile, ProductImages, Tag, ProductSpecifications, Sale, PaymentType, \
    PaymentStatus, DeliveryType, Payment, Delivery, Order


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'parent']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'sale']


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'value']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'email', 'phone', 'avatar']


class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'discount', 'date_from', 'date_to']


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_express', 'express_price', 'base_less_than', 'base_price']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'status', 'error_message', 'card_number']


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'city', 'address']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_cost', 'payment', 'delivery']


admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductSpecifications, ProductSpecificationsAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
admin.site.register(PaymentStatus, PaymentStatusAdmin)
admin.site.register(DeliveryType, DeliveryTypeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Order, OrderAdmin)

