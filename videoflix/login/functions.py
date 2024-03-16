
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.utils.html import strip_tags
from .tokens import account_activation_token  
from django.core.mail import EmailMultiAlternatives


def send_register_mail(user):
    subject = 'Bitte bestätige deine Registierung'

    context = {
        'user': user,
        'domain': '127.0.0.1:8000',
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
    send_mail(
        subject=subject,
        message=strip_tags(message),  # Set message as empty string since you're sending HTML content
        html_message=message,  # Pass HTML content to html_message parameter
        from_email=from_email,
        recipient_list=recipient_list,
    )
    """