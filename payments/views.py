from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Transaction
from .sslcommerz import sslcommerz_payment_gateway

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # We expect amount and optionally a name
        amount = request.data.get('amount')
        name = request.data.get('name', request.user.get_full_name() or request.user.username)
        
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # The sslcommerz_payment_gateway function returns the gateway URL
            gateway_url = sslcommerz_payment_gateway(request, name, amount)
            return Response({"gateway_url": gateway_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutSuccessView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            Transaction.objects.create(
                name=data.get('value_a', ''),
                tran_id=data.get('tran_id'),
                val_id=data.get('val_id'),
                amount=data.get('amount'),
                card_type=data.get('card_type'),
                card_no=data.get('card_no'),
                store_amount=data.get('store_amount'),
                bank_tran_id=data.get('bank_tran_id'),
                status=data.get('status'),
                tran_date=data.get('tran_date'),
                currency=data.get('currency'),
                card_issuer=data.get('card_issuer'),
                card_brand=data.get('card_brand'),
                card_issuer_country=data.get('card_issuer_country'),
                card_issuer_country_code=data.get('card_issuer_country_code'),
                verify_sign=data.get('verify_sign'),
                verify_sign_sha2=data.get('verify_sign_sha2'),
                currency_rate=data.get('currency_rate'),
                risk_title=data.get('risk_title'),
                risk_level=data.get('risk_level'),
            )
            # Redirect to React Frontend Success Page
            return redirect(f"{settings.FRONTEND_URL}/payment/success")
        except Exception as e:
            # If transaction fails to save, redirect to failure page or return error string
            return redirect(f"{settings.FRONTEND_URL}/payment/fail")

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutFailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # SSLCommerz posts data even on failure
        return redirect(f"{settings.FRONTEND_URL}/payment/fail")

@method_decorator(csrf_exempt, name='dispatch')
class CheckoutCancelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return redirect(f"{settings.FRONTEND_URL}/payment/cancel")