from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from .models import CustomUser

User = CustomUser

def signup(request):
    if request.method=='POST':
        user_id = request.POST.get('user_id', '')
        user_pw = request.POST.get('user_pw', '')
        user_pw2 = request.POST.get('user_pw2', '')
        user_email = request.POST.get('user_email', '')
        user_name = request.POST.get('user_name', '')
        user_nickname = request.POST.get('user_nickname', '')
        user_gender = request.POST.get('user_gender', '')
        user_profile_pic = request.FILES.get('user_profile_pic', None)
        user_bio = request.POST.get('user_bio', '')
        user_type = request.POST.get('user_user_type', '')
        user_birth_date = request.POST.get('user_birth_date', '')

        if user_pw != user_pw2:
            messages.warning(request, "비밀번호가 다릅니다.")
        elif User.objects.filter(user_id=user_id).exists():
          messages.warning(request, "아이디가 중복됩니다.")
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
            messages.success(request, "회원가입 완료!")
            return redirect('/sign/login')
        return render(request,'signup.html')
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        user_id=request.POST.get('user_id')
        user_pw=request.POST.get('user_pw')
        user=authenticate(request,user_id=user_id,password=user_pw)
        if user is not None:
            auth.login(request,user)
            return redirect('/board/home')
        else:
            messages.warning(request, "아이디와 비밀번호를 확인해주세요.")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/sign/login')

