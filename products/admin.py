from django.contrib import admin
from .models import Category, Product,Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "seller", "price", "category", "created_at")
    list_filter = ("category", "seller")
    search_fields = ("name", "description")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rating", "created_at")



