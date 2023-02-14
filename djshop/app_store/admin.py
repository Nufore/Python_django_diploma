from django.contrib import admin
from .models import ProductCategory, Product, ProductPictures, Feedback


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price']


class ProductPicturesAdmin(admin.ModelAdmin):
    list_display = ['product', 'id']


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'added_at']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPictures, ProductPicturesAdmin)
admin.site.register(Feedback, FeedBackAdmin)

