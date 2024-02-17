from django.shortcuts import render
from rest_framework import permissions, viewsets
from django.http import HttpResponse
from .serializers import VideoSerializer
from .models import Video

# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def postVideo(self, request, *args, **kwargs):
        title = request.data['title']
        description = request.data['description']
        video_file = request.data['video_file']
        poster_file = request.data['poster_file']
        genre = request.data['genre']

        Video.objects.create(title=title, description = description,
                             video_file = video_file, poster_file = poster_file,
                             genre = genre)
        return HttpResponse({'message': 'Video has been added'}, status=200)