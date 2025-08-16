from rest_framework import serializers
from .models import Category,Product



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug"]
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category",write_only = True
    )
    
    class Meta:
        model = Product
        fields = [
            "id","title","description","price","stock",
            "image","created_at","category","category_id"
        ]



