from django.contrib import admin
from .models import Category, Product, Profile, ProductImages, Tag, ProductSpecifications, Sale


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


admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductSpecifications, ProductSpecificationsAdmin)
admin.site.register(Sale, SaleAdmin)
