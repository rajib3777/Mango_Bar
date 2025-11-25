from django.urls import path
from . import api_views

app_name = 'accounts'
urlpatterns = [
    path('register/', api_views.RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', api_views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', api_views.LoginView.as_view(), name='login'),
    path('logout/', api_views.LogoutView.as_view(), name='logout'),
    path('profile/', api_views.ProfileView.as_view(), name='profile'),
]


