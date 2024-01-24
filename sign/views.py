from django.shortcuts import render,redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User #django의 기본 user 모델 사용(models.py의 모델 X)

def signup(request):
	#메서드 POST인 경우
    if request.method=='POST':
       #사용자가 입력한 값을 변수에 저장한다.
        user_id=request.POST.get('id','')
        user_pw=request.POST.get('pwd','')
        user_pw2=request.POST.get('pwd2','')
        user_email=request.POST.get('email','')
        #비밀번호와 비밀번호 확인 값이 다른 경우
        if user_pw!=user_pw2:
            messages.warning(request, "비밀번호가 다릅니다.")
        #아이디가 중복되는 경우
        elif User.objects.filter(username=user_id).exists():
            messages.warning(request, "아이디가 중복됩니다.")
        #문제 없이 정상적인 경우
        else:
        	#회원 생성
            user= User.objects.create_user(
                username=user_id,
                password=user_pw,
                email=user_email,
            )
            messages.success(request, "회원가입 완료!")
            #로그인 페이지로 이동
            return redirect('/sign/login')
        return render(request,'signup.html')
    else:
        return render(request,'signup.html')
    return render(request,'signup.html')

def login(request):
	#메서드가 POST인 경우
    if request.method=='POST':
        user_id=request.POST['id']
        user_pw=request.POST['pwd']
        #해당 id,pw에 해당되는 유저를 확인
        user=authenticate(request,username=user_id,password=user_pw)
        if user is not None:
        	#유저 있는 경우 로그인 후 홈으로 이동
            auth.login(request,user)
            return redirect('/home')
        else:
        	#유저 없는 경우 메시지 출력
            messages.warning(request, "아이디와 비밀번호를 확인해주세요.")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logout(request):
	#로그아웃
    auth.logout(request)
    return redirect('/sign/login')