from django.dispatch import receiver
from login.functions import send_RestPassword_mail
from django_rest_passwordreset.signals import reset_password_token_created
import django_rq

"""
Sends reset password mail to user
"""
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # SEND EMAIL FOR REGISTRATION WITH RQ WORKER 
    queueResetPassword=django_rq.get_queue('default', autocommit=True)
    queueResetPassword.enqueue(send_RestPassword_mail, reset_password_token)
