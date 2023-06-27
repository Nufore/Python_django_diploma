from django.contrib import admin
from .models import ProductCategory, Product


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'added_at', 'name', 'description', 'picture']


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
