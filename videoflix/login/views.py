import json
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework import generics

from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

class CustomAuthToken(ObtainAuthToken):

    """
    CHECK login credentials and return Token
    """
    def post(self, request, *args, **kwargs):

        user = User.objects.get(email=request.data['email'])
        request.data['username'] = user.username
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        responseJSON = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        }
        return HttpResponse(json.dumps(responseJSON), content_type='application/json')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

"""
Activate User via Email Link
"""
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(os.getenv("FRONTEND_HOST"))
    else:
        return HttpResponse('Activation link is invalid!')

"""
Check if user Token is valid
"""
def check_token_view(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(email=data['email'])
        userToken = Token.objects.get(user=user)
        if data['token'] == userToken.key: 
             return JsonResponse({'valid': True})
    return JsonResponse({'valid': False})









