from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import VideoSerializer
from .models import Video
from rest_framework.views import APIView
import os

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

    class VideoQualityAPIView(APIView):
        def get(self, request, video_id, quality):
            video = Video.objects.get(pk=video_id)
            if quality == '480p':
                file_path = video.video_480p_file.path
            elif quality == '720p':
                file_path = video.video_720p_file.path
            else:
                file_path = video.video_file.path

            with open(file_path, 'rb') as file:
                response = Response(file.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
                return response