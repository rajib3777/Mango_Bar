from .models import Cart, CartItem
from rest_framework import serializers
from products.serializers import ProductSerializer




class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_detail = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_detail', 'quantity', 'price_per_item', 'total_price']
        read_only_fields = ['product_name', 'product_detail', 'total_price']

    def get_product_detail(self, obj):
        try:
            return ProductSerializer(obj.product, context=self.context).data
        except Exception:
            return None

    def get_total_price(self, obj):
        return obj.total_price()

        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 'created_at']
        read_only_fields = ['created_at']
    

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_items(self, obj):
        return obj.total_items()
    
