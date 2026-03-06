from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .extra_api import OrderViewSet, OrderItemViewSet, update_order_status
from .api_views import buy_now


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r"order-items", OrderItemViewSet, basename="orderitem")


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/buy-now/', buy_now, name='api-buy-now'),
    path('api/orders/<int:order_id>/status/', update_order_status, name='api-update-order-status'),
    
]



