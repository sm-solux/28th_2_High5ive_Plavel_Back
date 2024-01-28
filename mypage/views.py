from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def my_info(request):

    # 현재 로그인한 사용자를 context에 추가합니다.
    current_user = request.user
    if current_user.is_authenticated:
        # 로그인한 상태라면, 현재 사용자의 정보를 context에 추가합니다.
        context = {
            'current_user_name': current_user.username,
            'current_user_nickname': current_user.nickname,
            'current_user_email': current_user.email,
            'current_user_gender': current_user.gender,
            'current_user_birth': current_user.birth_date,
            'current_user_bio': current_user.bio,
            'current_user_user_type': current_user.user_type,
            'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
        }
    else:
        # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
        context = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    return render(request, 'my_info.html', context)

@login_required
def my_posts(request):
    user = request.user
    my_posts = user.post_set.all()
    return render(request, 'my_posts.html', {'my_posts': my_posts})
