from rest_framework import serializers
from products.models import Product as Mango
from orders.models import Order, OrderItem
from django.contrib.auth import get_user_model

User = get_user_model()

class MangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('created_at',)
        
class OrderMangoSerializer(serializers.ModelSerializer):
    mango = serializers.StringRelatedField(read_only=True)
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created_at','total_price')
        
    
class MangoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = '__all__'
        read_only_fields = ('created_at',)
        
        
class OrderAdminSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)
    items = serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created_at','total_price')
        
        
class OrderItemAdminSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_per_item', 'total_price']
