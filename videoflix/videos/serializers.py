from rest_framework import serializers

from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'genre', 'video_file', 'poster_file']

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.video_file = validated_data.get('video_file', instance.video_file)
        instance.poster_file = validated_data.get('poster_file', instance.poster_file)
        instance.save()
        return instance

