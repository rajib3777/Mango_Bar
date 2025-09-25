from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('api/', include('products.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    path('home/', TemplateView.as_view(template_name="home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('services/', TemplateView.as_view(template_name="services.html"), name='services'),
    path('contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),
    path('settings/', TemplateView.as_view(template_name="settings.html"), name='settings')
]



if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
