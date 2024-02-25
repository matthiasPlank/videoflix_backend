from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .serializers import VideoSerializer
from .models import Video
from rest_framework.views import APIView
from videos.signals import convert_480p, convert_720p
import os

# Create your views here.
class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def postVideo(self, request, *args, **kwargs):
        title = request.data['title']
        description = request.data['description']
        video_file = request.data['video_file']
        poster_file = request.data['poster_file']
        genre = request.data['genre']

        video_instance = Video(title=title, description=description, video_file=video_file, poster_file=poster_file, genre=genre)

        # Perform validation (e.g., file type, size) before saving
        try:
            video_instance.full_clean()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Save the video instance to get a primary key (id)
        video_instance.save()

        # Perform video conversion based on the new video_instance.id
        # convert_480p(video_instance.id, video_file.path)  # Assuming you are using Celery for asynchronous tasks
        # convert_720p(video_instance.id, video_file.path)

        return Response({'message': 'Video has been added and conversion started'}, status=status.HTTP_201_CREATED)

"""
class VideoQualityAPIView(APIView):
        def get(self, request, video_id, quality):
            try:
                 video = Video.objects.get(pk=video_id)

                 if quality == '480p' and video.video_480p_file:
                    file_path = video.video_480p_file.path
                 elif quality == '720p' and video.video_720p_file:
                    file_path = video.video_720p_file.path
                 else:
                    file_path = video.video_file.path

                 with open(file_path, 'rb') as file:
                    response = Response(file.read(), content_type='video/mp4')
                    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
                    return response

            except Video.DoesNotExist:
                  return Response({'error': 'Video not found'}, status=404)
"""