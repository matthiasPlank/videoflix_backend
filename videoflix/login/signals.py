from .tasks import convert_480p
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from videos.models import Video
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("video wurde gespeichert")
    if created:
        print("new video created")
        convert_480p(instance.video_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)