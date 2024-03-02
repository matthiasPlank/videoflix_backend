from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from videos.models import Video
from django.db.models.signals import post_save

class VideoSignalTests(TestCase):

    def setUp(self):
        # Provide the content of a real video file
        with open('media/videos/testvideos/ants.mp4', 'rb') as file:
            video_content = file.read()

        # Create a Video instance with the real video content
        video_file = SimpleUploadedFile("video.mp4", video_content, content_type="video/mp4")
        self.video = Video.objects.create(video_file=video_file)

    @patch('videos.signals.convert_480p')
    @patch('videos.signals.convert_720p')
    def test_video_post_save_method(self, mock_convert_720p, mock_convert_480p):
        # Call the post_save signal manually
        post_save.send(sender=Video, instance=self.video, created=True)

        # Assert that the convert_480p and convert_720p functions were called with the correct arguments
        mock_convert_480p.assert_called_once_with(self.video.video_file.path)
        mock_convert_720p.assert_called_once_with(self.video.video_file.path)

        # Refresh the instance from the database to get the latest changes
        self.video.refresh_from_db()
        self.assertTrue(self.video.video_file.path)

