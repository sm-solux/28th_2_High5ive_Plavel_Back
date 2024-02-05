from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

import json

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import UserSerializer, LoginUserSerializer, CreateUserSerializer

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer

User = CustomUser

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)

        user_id = data.get('user_id', '')
        user_pw = data.get('user_pw', '')
        user_pw2 = data.get('user_pw2', '')
        user_email = data.get('user_email', '')
        user_name = data.get('user_name', '')
        user_nickname = data.get('user_nickname', '')
        user_gender = data.get('user_gender', '')
        user_profile_pic = data.get('user_profile_pic', None)
        user_bio = data.get('user_bio', '')
        #user_type = data.get('user_user_type', '')
        user_type = data.get('user_type'),
        user_birth_date = data.get('user_birth_date', '')

        if user_pw != user_pw2:
            return JsonResponse({"message": "Passwords do not match"}, status=400)
        elif CustomUser.objects.filter(user_id=user_id).exists():
            return JsonResponse({"message": "User ID already exists"}, status=400)
        else:
            user = CustomUser.objects.create_user(
                user_id=user_id,
                password=user_pw,
                email=user_email,
                username=user_name,
                nickname=user_nickname,
                gender=user_gender,
                profile_pic=user_profile_pic,
                bio=user_bio,
                user_type=user_type,
                birth_date=user_birth_date,
            )
            user.save()
            return JsonResponse({"message": "Sign Up Successful"})
    else:
        return JsonResponse({"message": "Invalid HTTP method"}, status=400)



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user