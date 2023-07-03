from django.contrib import admin
from .models import Category, Product, Profile


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image', 'parent']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'price', 'added_at', 'name', 'description', 'picture']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'avatar']


admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)
