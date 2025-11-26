from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Count
from products.models import Mango
from orders.models import Order
from .serializers import MangoAdminSerializer, OrderAdminSerializer
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_overview(request):
    total_mangos = Mango.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.STATUS_PENDING).count()
    completed_orders = Order.objects.filter(status=Order.STATUS_COMPLETED).count()

    data = {
        'total_mangos': total_mangos,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    data = {
        'total_mangos': Mango.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status=Order.STATUS_PENDING).count(),
        'completed_orders': Order.objects.filter(status=Order.STATUS_COMPLETED).count(),
    }
    return Response(data)

@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def mango_list_create(request):
    if request.method == 'GET':
        qs = Mango.objects.all().order_by('-created_at')
        serializer = MangoAdminSerializer(qs, many=True)
        return Response(serializer.data)
    else:
        serializer = MangoAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def mango_detail(request, pk):
    mango = get_object_or_404(Mango, pk=pk)
    if request.method == 'GET':
        return Response(MangoAdminSerializer(mango).data)
    if request.method == 'PUT':
        serializer = MangoAdminSerializer(mango, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        mango.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders_list(request):
    qs = Order.objects.select_related('buyer','mango').order_by('-created_at')
    serializer = OrderAdminSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_set_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.data.get('status')
    if new_status not in dict(Order.STATUS_CHOICES):
        return Response({'detail':'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    prev = order.status
    order.status = new_status
    order.save()

    
    if new_status == Order.STATUS_COMPLETED:
        try:
            send_mail(
                subject=f"Your order #{order.pk} is Completed",
                message=f"Dear {order.buyer.get_full_name() or order.buyer},\n\nYour order #{order.pk} has been completed.\n\nRegards,\nMango Bar",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.buyer.email],
                fail_silently=True
            )
        except Exception:
            pass
    return Response(OrderAdminSerializer(order).data)