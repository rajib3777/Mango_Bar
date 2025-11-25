from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer
from django.db import transaction
from rest_framework import viewsets
from .serializers import OrderItemSerializer




# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def buy_now(request):
    
#     user = request.user
#     product_id = request.data.get('product_id')
#     quantity = int(request.data.get('quantity', 1))
    
#     if not product_id:
#         return Response({"detail": "product_id required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     product = get_object_or_404(Product, id=product_id)
    
#     if product.quantity < quantity:
#         return Response({"detail": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
    
#     with transaction.atomic():
#         order = Order.objects.create(user=user, total_amount=0)
#         price = product.price
#         OrderItem.objects.create(
#             order=order,
#             product=product,
#             product_name=getattr(product, 'name', str(product)),
#             quantity=quantity,
#             price_per_item=price
#         )
        
#         product.quantity = max(product.quantity - quantity, 0)
#         product.save()
#         order.total_amount = quantity * price
#         order.save()
        
#         try :
#             send_mail(
#                 subject=f"Order #{order.id} Confirmation",
#                 message=(
#                     f"Hello {user.email},\n\n"
#                     f"Your order has been placed successfully!\n\n"
#                     f"Order ID: {order.id}\n"
#                     f"Product: {product.name}\n"
#                     f"Quantity: {quantity}\n"
#                     f"Total Amount: {order.total_amount} BDT\n"
#                     f"Status: Pending\n\n"
#                     "Thank you for ordering from Mango Bar!"
#                 ),
                
#                 from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
#                 recipient_list=[user.email] if user.email else [],
#                 fail_silently=False,
#             )
#         except Exception as e:
            
#             print("Please Try again !")
#             print("Email failed:", e)
    
#     serializer = OrderSerializer(order, context={'request': request})
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_order_status(request, order_id):
    user = request.user
    if not user.is_staff:
        return Response({"detail":"Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)

    order = get_object_or_404(Order, id=order_id)
    status_val = request.data.get('status')
    if not status_val:
        return Response({"detail":"status required"}, status=status.HTTP_400_BAD_REQUEST)

    order.status = status_val
    order.save()
    
    if status_val.lower() == 'completed':
        try:
            send_mail(
                subject=f"Order #{order.id} Completed",
                message=f"Your order #{order.id} status is now Completed.",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[order.user.email] if getattr(order.user, "email", None) else [],
                fail_silently=True,
            )
        except Exception:
            pass

            
    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)



class OrderViewSet(viewsets.ModelViewSet):
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        


class OrderItemViewSet(viewsets.ModelViewSet):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)
    

