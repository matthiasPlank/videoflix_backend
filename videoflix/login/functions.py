
import os
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.utils.html import strip_tags
from .tokens import account_activation_token  
from django.core.mail import EmailMultiAlternatives

"""
Sends a email for registration to user
"""
def send_register_mail(user):
    subject = 'Bitte bestätige deine Registierung'
    context = {
        'user': user,
        'domain': os.getenv("BACKEND_HOST"),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }

    html_message = render_to_string('acc_active_email.html', context )
    plain_message = render_to_string('acc_active_email.txt' , context)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    msg = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()


"""
Sends a email for password reset to user
"""
def send_RestPassword_mail(reset_password_token): 
    print("INSIDE OF send_RestPassword_mail")
    subject = "Password Reset"
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}{}".format(
            os.getenv("FRONTEND_HOST") + '/password_reset/',
            reset_password_token.key)     
    }

    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)
    from_email = settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives( subject , email_plaintext_message, from_email, [reset_password_token.user.email])
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()   