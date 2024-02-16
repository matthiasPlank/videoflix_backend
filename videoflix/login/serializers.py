
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.sites.shortcuts import get_current_site  
from django.core.mail import EmailMessage  

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active = False, 
        )
        
        user.set_password(validated_data['password'])
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk)),  
        token = account_activation_token.make_token(user),  
        #print(uid)
        #print(token)

        send_mail(
    	    subject='Bitte bestätige deine Registierung',
            message=render_to_string('acc_active_email.html', {
                'user': user,  
                'domain': '127.0.0.1:8000',  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            }),  
    		from_email=settings.EMAIL_HOST_USER,
    		recipient_list=[user.email]
        )

        return user
