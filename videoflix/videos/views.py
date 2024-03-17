from django.conf import settings
from rest_framework import permissions, viewsets
from .serializers import VideoSerializer
from .models import Video
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows videos to be viewed or edited.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['genre']  # Exmaple http://127.0.0.1:8000/video?genre=Horror

    """
    Returns a list of video objects on an HTTP GET request
    """
    @method_decorator(cache_page(CACHE_TTL))  # CACHETTL should be defined in settings
    def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)