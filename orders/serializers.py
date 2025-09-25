from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart, CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_name', 'quantity', 'price_per_item']
        
    def get_total_price(self, obj):
        return obj.total_price()
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'product_name', 'quantity', 'order_date', 'items']
        
    def get_total_price(self, obj):
        return sum(item.total_price() for item in obj.items.all())
    
    
class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_name', 'quantity', 'price_per_item', 'total_price']
        
    def get_total_price(self, obj):
        return obj.total_price()
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_name', 'items', 'total_price']
        
    def get_total_price(self, obj):
        return obj.total_price()
