from django.urls import path
from .api_views import ProductDetailAPIView, ProductListCreateAPIView, CategoryListAPIView, search_products


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/search/', search_products, name='product-search'),
    
]




