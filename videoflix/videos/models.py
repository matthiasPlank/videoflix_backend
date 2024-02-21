from datetime import date
from django.db import models


GENRE_CHOICES = {
        'Drama': 'Drama',
        'Comedy': 'Comedy',
        'Action': 'Action',
        'Thriller': 'Thriller',
        'Horror': 'Horror',
        'Science Fiction': 'Science Fiction',
        'Fantasy': 'Fantasy',
        'Romance': 'Romance',
        'Adventure': 'Adventure',
        'Crime': 'Crime',
        'Animation': 'Animation',
        'Mystery': 'Mystery',
        'Documentary': 'Documentary',
        'Other' : 'Other'
}
class Video(models.Model):

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    video_file = models.FileField(upload_to='videos' , blank=True , null=True)
    video_480p_file = models.FileField(upload_to='videos/480p/', null=True, blank=True)
    video_720p_file = models.FileField(upload_to='videos/720p/', null=True, blank=True)
    poster_file = models.FileField(upload_to='poster' , blank=True , null=True)
    created_at = models.DateField(default=date.today)
    genre = models.CharField(max_length=32, choices=GENRE_CHOICES , default='Other')