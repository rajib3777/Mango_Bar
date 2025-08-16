from django.urls import path
from accounts.views import (
    sign_up, sign_in, sign_out,activate_user,
    # seller_dashboard,customer_dashboard,
    admin_dashboard,reset_password,reset_password_confirm,
    seller_dashboard, customer_dashboard, profile_view,
    UserPasswordChangeView, EditProfileView
)

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    
    path('activate/<str:uidb64>/<str:token>/',activate_user,name='activate-user'),
    
    
    path('seller-dashboard/', seller_dashboard, name='seller-dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),
    path('customer-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('profile/',profile_view, name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('profile/change-password/', UserPasswordChangeView.as_view(), name='change-password'),
    path('reset-password/',reset_password,name='reset-password'),
    path('reset/<uidb64>/<token>/',reset_password_confirm, name='password_reset_confirm'),
    
]