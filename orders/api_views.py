from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.serializers import CartSerializer, CartItemSerializer
from products.models import Product



class IsOwnerOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

    
    

class OrderViewSet(viewsets.ModelViewSet):
    
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
        
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('order__id')
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
        

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def buy_now(request):
    
    user = request.user
    product_id = request.data.get('product_id')
    
    if not product_id:
        return Response({"detail": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        quantity = int(request.data.get('quantity', 1))
    except Exception:
        return Response({"detail": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

    
    product = get_object_or_404(Product, id=product_id)
    
    stock_value = None
    if hasattr(product, 'quantity'):
        stock_value = product.quantity
    elif hasattr(product, 'stock'):
        stock_value = product.stock
    
    if stock_value is not None and stock_value < quantity:
        return Response({"detail": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

    
    
    with transaction.atomic():
        order = Order.objects.create(user=user, total_amount=0)
        price = getattr(product, 'price', 0)
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name if hasattr(product, 'name') else '',
            quantity=quantity,
            price_per_item=price
        )
        if hasattr(product, 'quantity'):
            product.quantity = max(product.quantity - quantity, 0 )
        elif hasattr(product, 'stock'):
            product.stock = max(product.stock - quantity, 0)
            
        product.save()
        order.total_amount = sum(item.total_price() for item in order.items.all())
        order.save()
        
    try:
        if getattr(settings, 'DEFAULT_FROM_EMAIL', None) and getattr(user, 'email', None):
            send_mail(
                subject=f"Order #{order.id} Confirmation",
                message=f"Your order #{order.id} has been placed. Total: {order.total_amount}. Status: {order.status}.",
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL'),
                recipient_list=[user.email],
                fail_silently=True,
            )
    except Exception:
        pass
    
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


    
    

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    status_val = request.data.get('status')
    if not status_val:
        return Response({"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST)

    order.status = status_val
    order.save()

    if status_val.lower() == 'completed':
        try:
            send_mail(
                subject=f"Order #{order.id} Completed",
                message=f"Your order #{order.id} has been marked as Completed.",
                from_email=f"{getattr(settings, 'DEFAULT_FROM_EMAIL', None)}",
                recipient_list=[order.user.email] if getattr(order.user, 'email', None) else [],
                fail_silently=True,
            )
        except Exception:
            pass
        
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)



    
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    



