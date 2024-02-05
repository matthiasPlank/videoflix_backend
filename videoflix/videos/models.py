from datetime import date
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    video_file = models.FileField(upload_to='videos' , blank=True , null=True)
    created_at = models.DateField(default=date.today)