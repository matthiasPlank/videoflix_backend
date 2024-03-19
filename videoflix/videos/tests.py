from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from videos.tasks import convert_480p, convert_720p
from videos.models import Video
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from rq import get_current_job
from django_rq import get_queue

from django.test import TestCase
from django_rq import get_queue
from unittest.mock import MagicMock
from django.core.cache import cache
from videos.models import Video
from videos.signals import video_post_save


from django.test import TestCase
from django_rq import get_worker


from django.test import TestCase
from django_rq import get_queue
from unittest.mock import patch

from django.test import TestCase
from django.core.cache import cache
from django_rq import get_queue
from unittest.mock import patch, Mock

class VideoSignalTests(TestCase):

    """
    Creates video object for test 
    """
    def setUp(self):
        # Provide the content of a real video file
        with open('media/videos/testvideos/ants.mp4', 'rb') as file:
            video_content = file.read()

        # Create a Video instance with the real video content
        video_file = SimpleUploadedFile("video.mp4", video_content, content_type="video/mp4")
        self.video = Video.objects.create(video_file=video_file)

    """
    Tests the video conversion rq function call after creating new video
    """
    @patch('videos.signals.convert_480p')
    @patch('videos.signals.convert_720p')
    @patch('django_rq.get_queue')
    @patch('videos.signals.cache.clear')
    def test_video_post_save(self, mock_cache_clear,  mock_get_queue, mock_convert_720p, mock_convert_480p):
        
        instance = Mock(video_file=Mock(path=self.video.video_file))

        mock_queue = Mock()
        mock_get_queue.return_value = mock_queue

        video_post_save(None, instance, created=True)

        mock_cache_clear.assert_called_once()
        mock_queue.enqueue.assert_any_call(mock_convert_480p, self.video.video_file)
        mock_queue.enqueue.assert_any_call(mock_convert_720p, self.video.video_file)

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


    def test_video_creation_missing_video_file(self):
    # Creating a video with a missing video_file
        video = Video(
        title='Test Video',
        description='Test description',
        video_file=None,
        created_at=date.today(),
        genre='Drama'
    )

        with self.assertRaises(ValidationError) as context:
            video.full_clean()

        error_dict = context.exception.error_dict
        error_messages = error_dict.get('video_file', [])
        if error_messages:
        # Check if the expected error message is in the list of error messages
            self.assertIn("This field cannot be blank.", str(error_messages))
        else:
        # If 'video_file' is not in error_dict, explicitly fail the test
            self.fail("ValidationError for 'video_file' not found")