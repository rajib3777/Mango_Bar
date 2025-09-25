from django.urls import path
from . import views





urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("add/", views.add_product, name="product_create"),
    path("update/<int:pk>/", views.product_update, name="product_update"),
    path("delete/<int:pk>/", views.product_delete, name="product_delete"),
    path("cart/remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update_stock/<int:product_id>/",views.update_product_quantity, name="update_product_quantity"),
]
