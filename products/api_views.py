from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__slug__iexact=category)
        return queryset


    def perform_create(self, serializer):
        serializer.save(Seller=self.request.user)
        
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def search_products(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
