from django.test import TestCase, SimpleTestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json  # Import json module
from django.urls import reverse, resolve
from .views import RegisterView, activate

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

class TestUrls(SimpleTestCase):

    def test_authRegister_url_is_resolved(self):
        url = reverse('auth_register')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_loginActivate_url_is_resolved(self):
        uidb64 = 'sample_uidb64'
        token = 'sample_token'

        url = reverse('activate', args=[uidb64, token])
        self.assertEqual(resolve(url).func, activate)



