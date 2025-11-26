from rest_framework import serializers
from products.models import Mango
from orders.models import Order
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
        