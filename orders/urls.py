from django.urls import path, include
from . import views, api_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r"order-items", api_views.OrderItemViewSet, basename="orderitem")
router.register(r"carts", api_views.CartViewSet, basename="cart")
router.register(r"cart-items", api_views.CartItemViewSet, basename="cartitem")


urlpatterns = [
    path("checkout/<int:cart_id>/", views.checkout, name="checkout"),
    path("list/", views.order_list, name="order_list"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),

    path("api/", include(router.urls))
    
]



