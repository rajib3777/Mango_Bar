from django.db import models

# Create your models here.

# Create your models here.
from django.db import models  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from order.models import CartItem, Order
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer
from django.shortcuts import get_object_or_404

# List all products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Retrieve a single product
@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# Add item to cart
@api_view(['POST'])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View cart items
@api_view(['GET'])
def view_cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)

# Remove item from cart
@api_view(['DELETE'])
def remove_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

# Place order
@api_view(['POST'])
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user, ordered=False)
    if not cart_items.exists():
        return Response({"error": "No items in cart"}, status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.create(user=request.user)
    for item in cart_items:
        item.ordered = True
        item.order = order
        item.save()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
