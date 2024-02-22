from .tasks import convert_480p, convert_720p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from videos.models import Video
import os

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@receiver(post_save, sender=Video)
@cache_page(CACHE_TTL)
def video_post_save(sender, instance, created, **kwargs):
    print("video wurde gespeichert")
    if created:
        if instance.video_480p_file:
            convert_480p.delay(instance.video_file.path, instance.video_480p_file.path)
        if instance.video_720p_file:
            convert_720p.delay(instance.video_file.path, instance.video_720p_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
        if instance.video_480p_file and os.path.isfile(instance.video_480p_file.path):
            os.remove(instance.video_480p_file.path)
        if instance.video_720p_file and os.path.isfile(instance.video_720p_file.path):
            os.remove(instance.video_720p_file.path)


#REST_PASSWORD
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}{}".format(
            'http://localhost:4200/password_reset/',
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()