from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from videos.models import Video
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

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


class VideoModelTest(TestCase):
    def setUp(self):
        # Create a test user (you can customize this according to your User model)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        with open('media/videos/testvideos/ants.mp4', 'rb') as file:
            video_content = file.read()
        # Create a test video file
        video_content = video_content
        self.video_file = SimpleUploadedFile("test_video.mp4", video_content, content_type="video/mp4")

    def test_video_creation(self):
        # Test creating a video with all required fields filled
        Video.objects.create(
            title='Test Video',
            description='Test description',
            video_file=self.video_file,
            created_at=date.today(),
            genre='Drama'
        )

        # Check if the video is saved in the database
        self.assertEqual(Video.objects.count(), 1)

    def test_video_creation_missing_title(self):
    # creating a video with a missing title
        video = Video(
        title='',
        description='Test description',
        video_file=self.video_file,
        created_at=date.today(),
        genre='Drama'
    )

        with self.assertRaises(ValidationError) as context:
             video.full_clean()

        error_dict = context.exception.error_dict
        # Get the error messages associated with the 'title' field
        error_messages = error_dict.get('title', [])
        # Check if there are error messages for the 'title' field
        if error_messages:
        # Check if the expected error message is in the list of error message
            self.assertIn("This field cannot be blank.", str(error_messages))
        else:
         # If 'title' is not in error_dict, explicitly fail the test
            self.fail("ValidationError for 'title' not found")

