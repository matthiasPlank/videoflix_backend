
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  

def send_register_mail(user):
    send_mail(
                subject='Bitte bestätige deine Registierung',
                message=render_to_string('acc_active_email.html', {
                    'user': user,  
                    'domain': '127.0.0.1:8000',  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                }),  
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )