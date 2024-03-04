from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json  # Import json module

class CustomAuthTokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_valid_login_credentials(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post('/api-token-auth/', data, format='json')

        self.assertEqual(response.status_code, 200)

        # Parse the JSON content from the response
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertIn('token', response_data)
        self.assertIn('user_id', response_data)
        self.assertIn('email', response_data)
        self.assertIn('username', response_data)

