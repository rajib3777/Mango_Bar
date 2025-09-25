from django.urls import path
from .api_views import ProductDetailAPIView,ProductListCreateAPIView,CategoryListAPIView,search_products


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categpries/',CategoryListAPIView.as_view(),name='category-list'),
    path('search/',search_products,name='product-search')
    
]




