import string
import random
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from .models import PaymentGateway



def generator_trangection_id( size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


    

def sslcommerz_payment_gateway(request, name, amount):
 
    gateway = PaymentGateway.objects.all().first()
    if not gateway:
        raise Exception("Payment Gateway credentials not configured in the database.")
        
    cradentials = {'store_id': gateway.store_id,
            'store_pass': gateway.store_pass, 'issandbox': True} 
            
    sslcommez = SSLCOMMERZ(cradentials)
    body = {}
    body['total_amount'] = amount
    body['currency'] = "BDT"
    body['tran_id'] = generator_trangection_id()
    
    # These URLs are what SSLCommerz hits with POST data (webhook-like)
    body['success_url'] = request.build_absolute_uri('/payments/success/')
    body['fail_url'] = request.build_absolute_uri('/payments/fail/')
    body['cancel_url'] = request.build_absolute_uri('/payments/cancel/')
    
    body['emi_option'] = 0
    body['cus_name'] = name
    
    # Try fetching details from request user, else use default dummy data for sandbox
    body['cus_email'] = request.user.email if hasattr(request, 'user') and request.user.is_authenticated else 'test@example.com'
    body['cus_phone'] = getattr(request.user, 'phone', '01711111111') if hasattr(request, 'user') and request.user.is_authenticated else '01711111111'
    body['cus_add1'] = getattr(request.user, 'address', 'Dhaka') if hasattr(request, 'user') and request.user.is_authenticated else 'Dhaka'
    body['cus_city'] = 'Dhaka'
    body['cus_country'] = 'Bangladesh'
    body['shipping_method'] = "NO"
    body['multi_card_name'] = ""
    body['num_of_item'] = 1
    body['product_name'] = "Test"
    body['product_category'] = "Test Category"
    body['product_profile'] = "general"
    body['value_a'] = name

    response = sslcommez.createSession(body)
    
    if "sessionkey" in response:
        return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]
    else:
        raise Exception("Failed to generate SSLCommerz session: " + str(response))