from django.urls import path
from . import views

urlpatterns = [
    # Product APIs
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # Cart APIs
    path('cart/', views.cart_items, name='cart-items'),

    # Order APIs
    path('orders/', views.order_list, name='order-list'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
]
