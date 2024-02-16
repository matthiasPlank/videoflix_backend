from rest_framework import serializers

from .models import Video

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Video
        fields = '__all__'

