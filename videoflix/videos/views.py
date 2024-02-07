from django.shortcuts import render
from rest_framework import permissions, viewsets

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