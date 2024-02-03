from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from board.models import Post
from django.http import JsonResponse

# Create your views here.

# # 회원 정보
# def my_info(request):

#     # 현재 로그인한 사용자를 context에 추가.
#     current_user = request.user
#     if current_user.is_authenticated:
#         # 로그인한 상태라면 현재 사용자의 정보를 context에 추가.
#         context = {
#             'current_user_name': current_user.username,
#             'current_user_nickname': current_user.nickname,
#             'current_user_email': current_user.email,
#             'current_user_gender': current_user.gender,
#             'current_user_birth': current_user.birth_date,
#             'current_user_bio': current_user.bio,
#             'current_user_user_type': current_user.user_type,
#             'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
#         }
#     else:
#         # 로그인하지 않은 상태면 사용자 정보를 비워둠.
#         context = {
#             'current_user_nickname': None,
#             'current_user_profile_pic': None,
#             'current_user_user_type': None,
#         }

#     return JsonResponse(user_info)


# #내가 쓴 글
# @login_required
# def my_posts(request):
#     user = request.user
#     my_posts = user.post_set.all().annotate(bookmark_count=Count('bookmarked'))
#     return render(request, 'my_posts.html', {'my_posts': my_posts})


# #댓글 단 글
# @login_required
# def my_comments(request):
#     user = request.user
#     my_comments = user.comment_set.all()
#     commented_posts = {comment.post for comment in my_comments}

#     # 북마크 카운트를 계산합니다.
#     for post in commented_posts:
#         post.bookmarks_count = post.bookmarked.count()
#     commented_posts = {comment.post for comment in my_comments}
#     return render(request, 'my_comments.html', {'commented_posts': commented_posts})

# 회원 정보
def my_info(request):
    # 현재 로그인한 사용자를 가져옵니다.
    current_user = request.user
    if current_user.is_authenticated:
        # 로그인한 상태라면 현재 사용자의 정보를 가져옵니다.
        user_info = {
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
        # 로그인하지 않은 상태라면 사용자 정보를 비워둡니다.
        user_info = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    return JsonResponse(user_info)

#내가 쓴 글
@login_required
def my_posts(request):
    user = request.user
    my_posts = user.post_set.all().annotate(bookmark_count=Count('bookmarked'),comments_count=Count('comments'))

    post_list = []
    for post in my_posts:
        post_dict = {
            'id': post.id,
            'author': post.author.nickname,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'bookmark_count': post.bookmark_count,
            'comments_count':post.comments_count,
        }
        post_list.append(post_dict)

    return JsonResponse({'my_posts': post_list}, safe=False)

#댓글 단 글
@login_required
def my_comments(request):
    user = request.user
    my_comments = user.comment_set.all().annotate(bookmark_count=Count('bookmarked'),comments_count=Count('comments'))
    commented_posts = {comment.post for comment in my_comments}

    # 북마크 카운트를 계산합니다.
    for post in commented_posts:
        post.bookmarks_count = post.bookmarked.count()

    post_list = []
    for post in commented_posts:
        post_dict = {
            'id': post.id,
            'author': post.author.nickname,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'bookmark_count': post.bookmarks_count,
            'comments_count':post.comments_count,
        }
        post_list.append(post_dict)

    return JsonResponse({'commented_posts': post_list}, safe=False)


def my_test(request):

    # 현재 로그인한 사용자를 context에 추가.
    current_user = request.user
    if current_user.is_authenticated:
        # 로그인한 상태라면 현재 사용자의 정보를 context에 추가.
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
        # 로그인하지 않은 상태면 사용자 정보를 비워둠.
        context = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    return render(request, 'my_test.html', context)