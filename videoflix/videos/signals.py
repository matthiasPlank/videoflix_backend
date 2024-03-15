
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from videos.tasks import convert_480p, convert_720p
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
from django.core.cache import cache
import django_rq

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

"""
Start video conversiona after new video is created in database
"""
#@cache_page(CACHE_TTL)
@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("video wurde gespeichert")
    if created:
        cache.clear(); 
        if instance.video_file:
            queue=django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert_480p, instance.video_file.path)
            queue.enqueue(convert_720p, instance.video_file.path)
            #convert_480p(instance.video_file.path)
            #convert_720p(instance.video_file.path)


"""
Deletes file from filesystem
when corresponding `MediaFile` object is deleted.
"""
@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            cache.clear(); 


