from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity', 'price_per_item')
    search_fields = ('product_name', 'order__id')
    