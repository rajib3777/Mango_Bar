from django.urls import path
from .api_views import ProductDetailAPIView, CategoryListAPIView, search_products

urlpatterns = [
    # Legacy routes using HTML templates are removed.
    
    # API endpoints are mostly handled in api_urls.py, but keeping these here for backward compatibility if referenced.
    path("api/<int:pk>/", ProductDetailAPIView.as_view(), name="api-product-detail"),
    path("api/categories/", CategoryListAPIView.as_view(), name="api-category-list"),
    path("api/search/", search_products, name="api-product-search"),
]
