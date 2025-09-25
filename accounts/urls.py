from django.urls import path
from accounts.views import sign_up, sign_in, sign_out, activate_user
from accounts.views import seller_dashboard, customer_dashboard, admin_dashboard
from accounts.views import profile_view, UserPasswordChangeView,edit_profile
from accounts.views import reset_password, reset_password_confirm ,user_profile
from accounts import api_views



urlpatterns = [
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("sign-out/", sign_out, name="logout"),
    
    
    path("activate/<str:uidb64>/<str:token>/", activate_user, name="activate-user"),
    
    path("seller-dashboard/", seller_dashboard, name="seller-dashboard"),
    path("customer-dashboard/", customer_dashboard, name="customer-dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("profile/<int:user_id>/", user_profile, name="user_profile"),
    
    
    path("profile/", profile_view, name="profile"),
    path("profile/edit/",edit_profile , name="edit-profile"),
    path("profile/change-password/", UserPasswordChangeView.as_view(), name="change-password"),
    path("reset-password/", reset_password, name="reset_password"),
    path("reset/<uidb64>/<token>/", reset_password_confirm, name="password_reset_confirm"),
    
    
    
    path("api/register/", api_views.RegisterAPIView.as_view(), name="api_register"),
    path("api/login/", api_views.LoginAPIView.as_view(), name="api_login"),
    path("api/logout/", api_views.LogoutAPIView.as_view(), name="api_logout"),
    path("api/user/",api_views.UserDetailAPIView.as_view(), name="api_user_detail"),
    
]