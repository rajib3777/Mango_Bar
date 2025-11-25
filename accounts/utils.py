from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    path = reverse('accounts:verify-email', kwargs={'uidb64': uid, 'token': token})
    verify_url = request.build_absolute_uri(path)
    subject = "Verify your MangoStore account"
    message = f"hello,\n\nClick the link to verify your account:\n{verify_url}\n\nThanks!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
    


