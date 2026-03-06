from django.urls import path
from .api_views import ProductDetailAPIView, CategoryListAPIView, search_products


urlpatterns = [
    # These are legacy and require templates. If needed, they should be converted to API views or removed.
    # path("", views.product_list, name="product_list"),
    # path("<int:pk>/", views.product_detail, name="product_detail"),
    
    # API endpoints are mostly handled in api_urls.py, but keeping these here for backward compatibility if referenced.
    path("api/<int:pk>/", ProductDetailAPIView.as_view(), name="api-product-detail"),
    path("api/categories/", CategoryListAPIView.as_view(), name="api-category-list"),
    path("api/search/", search_products, name="api-product-search"),
]
