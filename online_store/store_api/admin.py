from django.contrib import admin
from .models import Category, Product, Profile, ProductImages, Tag, ProductSpecifications, Sale, PaymentType, \
    PaymentStatus, DeliveryType, Payment, Delivery, Order, OrderList
from .forms import ProductAdminForm
from django.template.loader import get_template
from django.utils.translation import gettext as _


@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'parent']


class ProductImageInline(admin.TabularInline):
    model = ProductImages
    fields = ("productimage_thumbnail",)
    readonly_fields = ("productimage_thumbnail",)
    max_num = 0

    def productimage_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""
        tpl = get_template("store_api/admin/product_thumbnail.html")
        return tpl.render({"image": instance.image})
    productimage_thumbnail.short_description = _("Thumbnail")


class SpecificationsInline(admin.TabularInline):
    model = ProductSpecifications


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [
        ProductImageInline,
        SpecificationsInline,
    ]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_images(form.instance)
    # fieldsets = [
    #     (None, {
    #         'fields': ('title', 'description', 'fullDescription')
    #     }),
    #     ('Price & count', {
    #         'fields': ('price', 'count')
    #     }),
    #     ('Category & tags', {
    #         'fields': ('category', 'tags')
    #     }),
    #     ('Rating, reviews, freeDelivery, sale', {
    #         'fields': ('rating', 'reviews', 'freeDelivery', 'sale'),
    #         'classes': ('collapse',),
    #     }),
    # ]
    list_display = ['id', 'title', 'description', 'price', 'sale']
    list_display_links = ['id', 'title']
    # search_fields = 'title', 'description'


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ProductSpecifications)
class ProductSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'value']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'email', 'phone', 'avatar']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'discount', 'date_from', 'date_to']


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_express', 'express_price', 'base_less_than', 'base_price']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'status', 'error_message', 'card_number']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'city', 'address']


class OrderListInline(admin.TabularInline):
    model = OrderList


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderListInline,
    ]
    list_display = ['id', 'user', 'order_date', 'total_cost', 'payment', 'delivery']
