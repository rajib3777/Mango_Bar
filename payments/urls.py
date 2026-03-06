from django.urls import path
from .views import InitiatePaymentView, CheckoutSuccessView, CheckoutFailView, CheckoutCancelView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='payment-initiate'),
    path('success/', CheckoutSuccessView.as_view(), name='payment-success'),
    path('fail/', CheckoutFailView.as_view(), name='payment-fail'),
    path('cancel/', CheckoutCancelView.as_view(), name='payment-cancel'),
]