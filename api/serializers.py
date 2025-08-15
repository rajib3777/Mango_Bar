from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from mytailwind import views
from django.conf.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('_debug_/', include('debug_toolbar.urls')),
    path('api/products/', include('products.api_urls')),
    path('api/orders/', include('order.api_urls')),
    
    # Apps
    path('', include('mytailwind.urls')),         
    path('', include('users.urls')),              
    path('mango/', include('mango.urls')), 
    path('orders/', include('orders.urls')),       
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # Payment views
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
]