from django.urls import path
from accounts.views import (
    sign_up, sign_in, sign_out,activate_user,
    # seller_dashboard,customer_dashboard,
    admin_dashboard
    # profile_view,
    # Editprofileview, Userpasswordchangeview,
    # Userpasswordresetview, Userpasswordresetconfirmview
)

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    
    path('activate/<str:uidb64>/<str:token>/',activate_user,name='activate-user'),
    
    
    # path('seller-dashboard/', seller_dashboard, name='seller-dashboard'),
    # path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),
    path('customer-dashboard/', admin_dashboard, name='admin_dashboard'),
    # path('profile/',profile_view, name='profile'),
    # path('profile/edit/', Editprofileview.as_view(), name='edit-profile'),
    # path('profile/change-password/', Userpasswordchangeview.as_view(), name='change-password'),
    # path('reset-password/', Userpasswordresetview.as_view(),name='reset-password'),
    # path('reset/<uidb64>/<token>/', Userpasswordresetconfirmview.as_view(), name='password_reset_confirm'),
    
]