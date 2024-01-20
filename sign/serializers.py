from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_email', 'user_pw', 'user_name', 'user_register_dttm']
