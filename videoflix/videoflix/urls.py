"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from login import views as loginView
from videos import views as videoView
from django.urls import path
from videos.views import VideoQualityAPIView



router = routers.DefaultRouter()
router.register(r'video', videoView.VideoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', loginView.CustomAuthToken.as_view()),
    path('register/', loginView.RegisterView.as_view(), name='auth_register'),
    path('activate/<str:uidb64>/<str:token>/', loginView.activate, name='activate'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/video/<int:video_id>/<str:quality>/', VideoQualityAPIView.as_view(), name='video_quality_api'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += router.urls
