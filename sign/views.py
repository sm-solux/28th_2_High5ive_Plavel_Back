from django.shortcuts import render,redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import User

# Create your views here.

def login(request):
    if request.method=='POST':
        user_email=request.POST['email']
        user_pw=request.POST['pwd']
        try:
            # 해당 이메일에 해당하는 유저를 가져옵니다.
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            # 해당 이메일을 가진 유저가 없는 경우
            messages.warning(request, "이메일과 비밀번호를 확인해주세요.")
            return render(request,'login.html')

        # 비밀번호를 확인합니다.
        if user.check_password(user_pw):
            # 비밀번호가 맞는 경우 로그인 후 홈으로 이동
            auth.login(request, user)
            return redirect('/home')
        else:
            # 비밀번호가 틀린 경우 메시지 출력
            messages.warning(request, "이메일과 비밀번호를 확인해주세요.")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
	#로그아웃
    auth.logout(request)
    return redirect('/sign/login')

def signup(request):
	#메서드 POST인 경우
    if request.method=='POST':
       #사용자가 입력한 값을 변수에 저장한다.
        user_id=request.POST.get('id','')
        user_pw=request.POST.get('pwd','')
        user_pw2=request.POST.get('pwd2','')
        user_email=request.POST.get('email','')
        user_name=request.POST.get('name','')
        #비밀번호와 비밀번호 확인 값이 다른 경우
        if user_pw!=user_pw2:
            messages.warning(request, "비밀번호가 다릅니다.")
        #아이디가 중복되는 경우
        elif User.objects.filter(email=user_email).exists():
            messages.warning(request, "이미 가입된 이메일입니다.")
        #문제 없이 정상적인 경우
        else:
        	#회원 생성
            user= User.objects.create_user(
                username=user_email,
                password=user_pw,
                email=user_email,
            )
            messages.success(request, "회원가입 완료!")
            #메인 페이지로 이동
            return redirect('/home')
        return render(request,'signup.html')
    else:
        return render(request,'signup.html')