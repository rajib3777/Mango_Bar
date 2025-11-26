from django.urls import path
from . import views



urlpatterns = [
    path('overview/', views.admin_overview, name='admin_overview'),
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('mangos/', views.mango_list_create, name='mango_list_create'),
    path('mangos/<int:pk>/', views.mango_detail, name='mango_detail'),
    path('orders/', views.admin_orders_list, name='admin_order_list'),
    path('orders/<int:pk>/set-status/', views.admin_set_order_status, name='admin_set_order_status'),
]

