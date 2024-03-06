from django.test import TestCase, SimpleTestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json

from django_rest_passwordreset.models import ResetPasswordToken
from django.urls import reverse, resolve
from .views import RegisterView, activate

class CustomAuthTokenTests(APITestCase):
    """
    Set up function was triggered foreach testcase - create new user
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    """
    Checks login credentials and returns token
    """
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
    
    
class RegisterTests(APITestCase):
    """
    Set up function was triggered foreach testcase - create new user
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    """
    Check registers new User with valid data
    """
    def test_registerNewUser(self): 
        data = {
            "email": "test@test.at",
            "password": "test_user", 
            "password2": "test_user",
            "username": "test@test.at"
        }
        response = self.client.post('/register/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 201)        

    """
    Check registers new User with invalid data (not same password)
    """
    def test_registerNewUserInvalidPassword(self): 
        data = {
            "email": "test@test.at",
            "password": "test_user", 
            "password2": "test_user123",
            "username": "test@test.at"
        }
        response = self.client.post('/register/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 400)       

class PasswordTests(APITestCase):
    """
    Set up function was triggered foreach testcase - create new user
    """
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    """
    Checks trigger for password reset for valid (created) mail/user
    """
    def test_resetPassword(self): 
        data = {
            "email": "test@example.com",
        }
        response = self.client.post('/password_reset/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 200)         

    """
    Checks trigger for password reset for invalid (not registered) mail/user
    """
    def test_resetPasswordInvalidMail(self): 
        data = {
            "email": "test@test.com",
        }
        response = self.client.post('/password_reset/' , data=json.dumps(data) , content_type='application/json') 
        self.assertEqual(response.status_code, 400)       

    """
    Sends a passwordreste request to create reset token. Gets token from db and checks if confirm api works
    """
    def test_changePassword(self):
        dataReset = {
            "email": "test@example.com",
        }
        response = self.client.post('/password_reset/' , data=json.dumps(dataReset) , content_type='application/json') 
        user = User.objects.get(email='test@example.com')
        reset_token = ResetPasswordToken.objects.filter(user=user).first()
        if reset_token:
            token_key = reset_token.key
            data = {
                "password": "MyNewPassword",
                "token" : token_key
            }
            response = self.client.post('/password_reset/confirm/' , data=json.dumps(data) , content_type='application/json') 
            self.assertEqual(response.status_code, 200)    
        else:
            pass

        
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



