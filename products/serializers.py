from rest_framework import serializers
from .models import Category,Product



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug"]
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category",write_only = True, required=False
    )
    
    Seller = serializers.StringRelatedField(read_only=True)
    
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "Seller",
            "price",
            "stock",
            # "quantity",
            "image",
            "created_at",
            "category",
            "category_id"
        ]
        read_only_fields = ["id","created_at","category","Seller"]
        
        





