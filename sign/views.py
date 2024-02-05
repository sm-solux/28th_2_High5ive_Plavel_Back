# from django.shortcuts import render, redirect
# from django.contrib import auth, messages
# from django.contrib.auth import authenticate, login as auth_login
# from .models import CustomUser
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import get_token

# import json

# from rest_framework import viewsets, permissions, generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from knox.models import AuthToken
# from .serializers import UserSerializer, LoginUserSerializer, CreateUserSerializer

# User = CustomUser

# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"message": "Invalid JSON format"}, status=400)

#         user_id = data.get('user_id', '')
#         user_pw = data.get('user_pw', '')
#         user_pw2 = data.get('user_pw2', '')
#         user_email = data.get('user_email', '')
#         user_name = data.get('user_name', '')
#         user_nickname = data.get('user_nickname', '')
#         user_gender = data.get('user_gender', '')
#         user_profile_pic = data.get('user_profile_pic', None)
#         user_bio = data.get('user_bio', '')
#         user_type = data.get('user_user_type', '')
#         user_birth_date = data.get('user_birth_date', '')

#         if user_pw != user_pw2:
#             return JsonResponse({"message": "Passwords do not match"}, status=400)
#         elif CustomUser.objects.filter(user_id=user_id).exists():
#             return JsonResponse({"message": "User ID already exists"}, status=400)
#         else:
#             user = CustomUser.objects.create_user(
#                 user_id=user_id,
#                 password=user_pw,
#                 email=user_email,
#                 username=user_name,
#                 nickname=user_nickname,
#                 gender=user_gender,
#                 profile_pic=user_profile_pic,
#                 bio=user_bio,
#                 user_type=user_type,
#                 birth_date=user_birth_date,
#             )
#             user.save()
#             return JsonResponse({"message": "Sign Up Successful"})
#     else:
#         return JsonResponse({"message": "Invalid HTTP method"}, status=400)

    
# # @csrf_exempt
# # def signup(request):
# #     if request.method=='POST':
# #         user_id = request.POST.get('user_id', '')
# #         user_pw = request.POST.get('user_pw', '')
# #         user_pw2 = request.POST.get('user_pw2', '')
# #         user_email = request.POST.get('user_email', '')
# #         user_name = request.POST.get('user_name', '')
# #         user_nickname = request.POST.get('user_nickname', '')
# #         user_gender = request.POST.get('user_gender', '')
# #         user_profile_pic = request.FILES.get('user_profile_pic', None)
# #         user_bio = request.POST.get('user_bio', '')
# #         user_type = request.POST.get('user_user_type', '')
# #         user_birth_date = request.POST.get('user_birth_date', '')

# #         if user_pw != user_pw2:
# #             messages.warning(request, "비밀번호가 다릅니다.")
# #         elif User.objects.filter(user_id=user_id).exists():
# #           messages.warning(request, "아이디가 중복됩니다.")
# #         else:
# #             user = CustomUser.objects.create_user(
# #                 user_id=user_id,
# #                 password=user_pw,
# #                 email=user_email,
# #                 username=user_name,
# #                 nickname=user_nickname,
# #                 gender=user_gender,
# #                 profile_pic=user_profile_pic,
# #                 bio=user_bio,
# #                 user_type=user_type,
# #                 birth_date=user_birth_date,
# #             )

# #             user.save()
# #             messages.success(request, "회원가입 완료!")
# #             return redirect('/sign/login')
# #         return render(request,'signup.html')
# #     else:
# #         return render(request,'signup.html')


# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             user_pw = data.get('user_pw')
#         except json.JSONDecodeError:
#             return JsonResponse({"message": "Invalid JSON format"}, status=400)

#         user = authenticate(request, username=user_id, password=user_pw)
#         if user is not None:
#             auth_login(request, user)
#             #token = AuthToken.objects.create(user)[1]
#             csrf_token = get_token(request)
#             return JsonResponse({"message": "Login Successful", "token": csrf_token})
#         else:
#             return JsonResponse({"message": "Check your ID and password"}, status=400)
#     else:
#         return JsonResponse({"message": "Invalid HTTP method"}, status=400)
    


    
    


# # class signup(APIView):
# #     serializer_class = CreateUserSerializer

# #     def post(self, request, *args, **kwargs):
# #         if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
# #             body = {"message": "short field"}
# #             return Response(body, status=status.HTTP_400_BAD_REQUEST)
# #         serializer = self.get_serializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         user = serializer.save()
# #         return Response(
# #             {
# #                 "user": UserSerializer(
# #                     user, context=self.get_serializer_context()
# #                 ).data,
# #                 "token": AuthToken.objects.create(user),
# #             }
# #         )


# # class login(APIView):
# #     serializer_class = LoginUserSerializer

# #     def post(self, request, *args, **kwargs):
# #         serializer = self.get_serializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         user = serializer.validated_data
# #         return Response(
# #             {
# #                 "user": UserSerializer(
# #                     user, context=self.get_serializer_context()
# #                 ).data,
# #                 "token": AuthToken.objects.create(user)[1],
# #             }
# #         )
    
# @csrf_exempt
# def logout(request):
#     auth.logout(request)
#     return redirect('/sign/login')


# # # 테스트 결과 받아오기
# # @csrf_exempt
# # def set_user_type(request):
# #     if request.method == 'POST':
# #         data = json.loads(request.body)
# #         user_type = data.get('user_type')
# #         # user_type을 사용하여 필요한 작업 수행...
# #         return JsonResponse({'status': 'success'}, status=200)
# #     else:
# #         return JsonResponse({'status': 'fail'}, status=400)

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer

# Create your views here.



# class RegistrationAPI(generics.GenericAPIView):
#     serializer_class = CreateUserSerializer

#     def post(self, request, *args, **kwargs):
#         if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
#             body = {"message": "short field"}
#             return Response(body, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {
#                 "user": UserSerializer(
#                     user, context=self.get_serializer_context()
#                 ).data,
#                 "token": AuthToken.objects.create(user),
#             }
#         )
    
    
# class RegistrationAPI(APIView):
#     serializer_class = CreateUserSerializer

#     def post(self, request, *args, **kwargs):
#         if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
#             body = {"message": "short field"}
#             return Response(body, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {
#                 "user": UserSerializer(
#                     user, context=self.get_serializer_context()
#                 ).data,
#                 "token": AuthToken.objects.create(user),
#             }
#         )
    

class RegistrationAPI(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user),
            }
        )



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