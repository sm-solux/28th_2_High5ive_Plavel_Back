from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import Post
from sign.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_pic', 'user_type'] 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
