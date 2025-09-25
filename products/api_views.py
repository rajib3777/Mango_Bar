from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from django.shortcuts import get_object_or_404


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(Seller=self.request.user)
        
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    

@api_view
@permission_classes([permissions.AllowAny])
def search_products(request):
    query = request.GET.het("q", "")
    products = Product.objects.filter(name_icontains=query) if query else Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
