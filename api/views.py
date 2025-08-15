from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from mango.models import Mango, MangoCategory
from orders.models import CartItem, Order
from .serializers import MangoSerializer, MangoCategorySerializer, CartItemSerializer, OrderSerializer
from mango.models import Product
from orders.models import CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404
from mango.models import Product
from orders.models import CartItem, Order
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer


# ================================
# Product Views (Search + Filter)
# ================================

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        # Query Parameters
        query = request.GET.get('q', '').strip()
        category_filter = request.GET.get('option1', '').strip()

        products = Product.objects.all()

        # Search by name or description
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        # Filter by category name
        if category_filter:
            products = products.filter(category__name__iexact=category_filter)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_cart_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)


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
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def cart_items(request):
    if request.method == 'GET':
        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'POST'])
def mango_category_list(request):
    if request.method == 'GET':
        categories = MangoCategory.objects.all()
        serializer = MangoCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MangoCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def mango_category_detail(request, pk):
    try:
        category = MangoCategory.objects.get(pk=pk)
    except MangoCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MangoCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MangoCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def mango_list(request):
    mangoes = Mango.objects.all()
    serializer = MangoSerializer(mangoes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def mango_detail(request, pk):
    try:
        mango = Mango.objects.get(pk=pk)
    except Mango.DoesNotExist:
        return Response({'error': 'Mango not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MangoSerializer(mango)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MangoSerializer(mango, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    elif request.method == 'DELETE':
        mango.delete()
        return Response({'message': 'Mango deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def mango_category_products(request, category_id):
    try:
        category = MangoCategory.objects.get(pk=category_id)
    except MangoCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



    

    