from rest_framework import serializers
from sign.models import CustomUser

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_type']