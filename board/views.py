# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post
from django.db.models import Count
# from .forms import CommentForm, PostForm
# from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# import datetime
from django.http import JsonResponse
# from .models import Post
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import PostSerializer, UserSerializer
# from datetime import datetime
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# def user_to_dict(user):
#     return {
#         'username': user.nickname,
#         'email': user.email,
#         'user_type': user.user_type,
#     }

# # 글 목록 (최신글) 
# # 댓글 수, 북마크 수 추가.
# def post_list(request):
#     posts = Post.objects.annotate(bookmark_count=Count('bookmarked', distinct=True),comments_count=Count('comments')).order_by('-created_at')
    
#     post_list = []
#     for post in posts:
#         post_dict = {
#             'id': post.id,
#             'author': post.author.nickname,
#             'title': post.title,
#             'usertype':post.author.user_type,
#             'content': post.content,
#             'created_at': post.created_at,
#             'updated_at': post.updated_at,
#             'comments_count': post.comments_count,
#             'bookmark_count': post.bookmark_count,
#         }
#         post_list.append(post_dict)
    
#     # 현재 로그인한 사용자를 가져옵니다.
#     current_user = request.user

#     # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
#     if current_user.is_authenticated:
#         user_info = {
#             'current_user_nickname': current_user.nickname,
#             'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
#             'current_user_user_type': current_user.user_type,
#         }
#     else:
#         # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
#         user_info = {
#             'current_user_nickname': None,
#             'current_user_profile_pic': None,
#             'current_user_user_type': None,
#         }

#     return JsonResponse({'posts': post_list, 'user_info': user_info}, safe=False)


# # 글 목록 (인기글)
# def post_list2(request):
#     posts = Post.objects.annotate(bookmark_count=Count('bookmarked', distinct=True),comments_count=Count('comments')).order_by('-bookmark_count', '-comments_count')

    
#     post_list = []
#     for post in posts:
#         post_dict = {
#             'id': post.id,
#             'author': post.author.nickname,
#             'title': post.title,
#             'usertype':post.author.user_type,
#             'content': post.content,
#             'created_at': post.created_at,
#             'updated_at': post.updated_at,
#             'comments_count': post.comments_count,
#             'bookmark_count': post.bookmark_count,
#         }
#         post_list.append(post_dict)
    
#     # 현재 로그인한 사용자를 가져옵니다.
#     current_user = request.user

#     # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
#     if current_user.is_authenticated:
#         user_info = {
#             'current_user_nickname': current_user.nickname,
#             'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
#             'current_user_user_type': current_user.user_type,
#         }
#     else:
#         # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
#         user_info = {
#             'current_user_nickname': None,
#             'current_user_profile_pic': None,
#             'current_user_user_type': None,
#         }

#     return JsonResponse({'posts': post_list, 'user_info': user_info}, safe=False)


# 글 필터링
def post_to_dict(post):
    return {
        'id': post.id,
        'author_nickname': post.author.username,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
        'author_type':post.author.user_type,
        'comment_count': post.comments_count,  # 댓글 수 추가
        'bookmark_count': post.bookmark_count,  # 북마크 수 추가
    }

def post_filter(request):
    user_type = request.GET.get('user_type', '')
    if user_type:
        posts = Post.objects.filter(author__user_type=user_type)
    else:
        posts = Post.objects.all()

    posts = posts.order_by('-created_at').annotate(bookmark_count=Count('bookmarked'), comments_count=Count('comments'))

    # 현재 로그인한 사용자를 가져옵니다.
    current_user = request.user

    # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
    if current_user.is_authenticated:
        user_info = {
            'current_user_nickname': current_user.nickname,
            'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
            'current_user_user_type': current_user.user_type,
        }
    else:
        # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
        user_info = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    posts = [post_to_dict(post) for post in posts]
    data = {
        'posts': posts,
        'user_info': user_info,
    }

    return JsonResponse(data)


# # 글 조회
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# #@login_required  # 로그인한 상태여야 조회 가능
# def post_detail(request, post_id):

#     post = get_object_or_404(Post, id=post_id)

#     # 현재 날짜를 얻습니다.
#     today = datetime.today()
#     # 생년월일이 있는 경우 나이를 계산합니다.
#     if post.author.birth_date:
#         # 나이 계산 로직
#         birth_date = datetime.strptime(post.author.birth_date, '%Y-%m-%d')
#         age = today.year - birth_date.year + 1
#     else:
#         age = None

#     bookmarks_count = post.bookmarked.count()

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user  # 현재 로그인한 사용자
#             comment.save()
#             return Response({
#                 'post_id': post.pk,
#                 'message': '댓글이 작성되었습니다.',
#             })
#     else:
#         form = CommentForm()

#     # 현재 로그인한 사용자를 context에 추가합니다.
#     current_user = request.user

#     if current_user.is_authenticated:
#         # 로그인한 상태라면, 현재 사용자의 정보를 context에 추가합니다.
#         context = {
#             'post': PostSerializer(post).data,
#             'age': age,
#             'gender': post.author.gender,
#             'nickname': post.author.nickname,
#             'usertype':post.author.user_type,
#             'bio':post.author.bio,
#             'profile_pic':post.author.profile_pic.url if post.author.profile_pic.url else None,
#             'bookmarks_count': bookmarks_count,
#             'current_user': UserSerializer(current_user).data,
#         }
#     else:
#         # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
#         context = {
#             'post': PostSerializer(post).data,
#             'age': age,
#             'gender': post.author.gender,
#             'nickname': post.author.nickname,
#             'usertype':post.author.user_type,
#             'bio':post.author.bio,
#             'profile_pic':post.author.profile_pic.url if post.author.profile_pic.url else None,
#             'bookmarks_count': bookmarks_count,
#             'current_user': None,
#         }

#     return Response(context)

# # 글 작성
# #@login_required
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # 현재 로그인한 사용자 = author
#             post.save()
#             return JsonResponse({'post_id': post.pk})
#     else:
#         return JsonResponse({'error': 'This endpoint only supports POST requests.'})


# # # 수정
# # #@login_required
# # def post_edit(request, post_id):
# #     post = get_object_or_404(Post, id=post_id)
# #     if request.user != post.author:
# #         return HttpResponseForbidden()  # 작성자가 아니면 403 Forbidden 응답을 반환.
    
# #     if request.method == "POST":
# #         form = PostForm(request.POST, request.FILES, instance=post)
# #         if form.is_valid():
# #             if 'image1' in request.FILES:
# #                 post.image1 = request.FILES['image1']
# #             if 'image2' in request.FILES:
# #                 post.image2 = request.FILES['image2']
# #             if 'image3' in request.FILES:
# #                 post.image3 = request.FILES['image3']
# #             post.title = form.cleaned_data['title']
# #             post.content = form.cleaned_data['content']
# #             post.save()
# #             return redirect('post_detail', post.id)
# #     else:
# #         form = PostForm(instance=post)
# #     return render(request, 'post_edit.html', {'form': form, 'post': post})

# # # 수정_이미지 삭제
# # @login_required
# # def delete_image(request, post_id, image_field):
# #     post = get_object_or_404(Post, id=post_id)
# #     if request.user != post.author:
# #         return HttpResponseForbidden()  # 작성자가 아니면 403 Forbidden 응답을 반환.
# #     getattr(post, image_field).delete()
# #     return redirect('post_edit', post.id)


# # # 삭제
# # @login_required
# # def post_delete(request, post_id):
# #     post = get_object_or_404(Post, id=post_id)
# #     if request.user != post.author:
# #         return HttpResponseForbidden()  # 작성자가 아니면 403 Forbidden 응답을 반환.
# #     post.delete()
# #     return redirect('post_list')

# # 북마크 기능
# @login_required
# def toggle_bookmark(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user in post.bookmarked.all():
#         post.bookmarked.remove(request.user)
#     else:
#         post.bookmarked.add(request.user)
#     return redirect('post_detail', post_id=post_id)

# # # 북마크된 글
# # @login_required
# # def bookmarked_posts(request):
# #     user = request.user
# #     bookmarks = user.bookmarked_posts.all()

# #     for post in bookmarks:
# #         post.bookmarks_count = post.bookmarked.count()

# #     return render(request, 'bookmarked_posts.html', {'bookmarks': bookmarks})


# # @login_required
# # def home(request):
# #     posts = Post.objects.annotate(
# #         bookmark_count=Count('bookmarked', distinct=True),
# #         comments_count=Count('comments', distinct=True)
# #     ).order_by('-bookmark_count', '-comments_count')
# #     return render(request, 'home.html', {'posts': posts})



# @login_required
# def post_edit(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user != post.author:
#         return JsonResponse({'error': 'Forbidden'}, status=403)

#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             return JsonResponse({'post_id': post.id})
#     else:
#         return JsonResponse({'error': 'This endpoint only supports POST requests.'}, status=400)


# @login_required
# def delete_image(request, post_id, image_field):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user != post.author:
#         return JsonResponse({'error': 'Forbidden'}, status=403)
#     getattr(post, image_field).delete()
#     return JsonResponse({'result': 'success'})


# @login_required
# def post_delete(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user != post.author:
#         return JsonResponse({'error': 'Forbidden'}, status=403)
#     post.delete()
#     return JsonResponse({'result': 'success'})


# @login_required
# def toggle_bookmark(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     if request.user in post.bookmarked.all():
#         post.bookmarked.remove(request.user)
#     else:
#         post.bookmarked.add(request.user)
#     return JsonResponse({'result': 'success'})


# @login_required
# def bookmarked_posts(request):
#     user = request.user
#     bookmarks = user.bookmarked_posts.all()
#     bookmarks = [post_to_dict(post) for post in bookmarks]
#     return JsonResponse({'bookmarks': bookmarks})


# @login_required
# def home(request):
#     posts = Post.objects.annotate(
#         bookmark_count=Count('bookmarked', distinct=True),
#         comments_count=Count('comments', distinct=True)
#     ).order_by('-bookmark_count', '-comments_count')
#     posts = [post_to_dict(post) for post in posts]
#     return JsonResponse({'posts': posts})

from django.urls import is_valid_path
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Post, Comment

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

Article = Post

# @api_view(['GET', 'POST'])
# def article_list(request):
#     if request.method == 'GET':
#         # articles = Article.objects.all()
#         articles = get_list_or_404(Article)
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED) 
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST'])
# def article_list(request):
#     current_user = request.user

#     # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
#     if current_user.is_authenticated:
#         user_info = {
#             'current_user_nickname': current_user.nickname,
#             'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
#             'current_user_user_type': current_user.user_type,
#         }
#     else:
#         # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
#         user_info = {
#             'current_user_nickname': None,
#             'current_user_profile_pic': None,
#             'current_user_user_type': None,
#         }

#     if request.method == 'GET':
#         # articles = Article.objects.all()
#         articles = get_list_or_404(Article)
#         serializer = ArticleListSerializer(articles, context={'request': request}, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(['GET', 'POST'])
def article_list(request):
    current_user = request.user

    # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
    if current_user.is_authenticated:
        user_info = {
            'current_user_nickname': current_user.nickname,
            'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
            'current_user_user_type': current_user.user_type,
        }
    else:
        # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
        user_info = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    if request.method == 'GET':
        # articles = Article.objects.all()
        articles = get_list_or_404(Article.objects.annotate(bookmark_count=Count('bookmarked', distinct=True),comment_count=Count('comments', distinct=True)).order_by('-created_at'))
        serializer = ArticleListSerializer(articles, context={'request': request}, many=True)
        data = {
            'articles': serializer.data,
            'user_info': user_info
        }
        return Response(data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'POST'])
def article_list2(request):
    current_user = request.user

    # 로그인한 상태라면, 현재 사용자의 정보를 가져옵니다.
    if current_user.is_authenticated:
        user_info = {
            'current_user_nickname': current_user.nickname,
            'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
            'current_user_user_type': current_user.user_type,
        }
    else:
        # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
        user_info = {
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    if request.method == 'GET':
        # articles = Article.objects.all()
        articles = get_list_or_404(Article.objects.annotate(bookmark_count=Count('bookmarked', distinct=True),comment_count=Count('comments', distinct=True)).order_by('-bookmark_count'))
        serializer = ArticleListSerializer(articles, context={'request': request}, many=True)
        data = {
            'articles': serializer.data,
            'user_info': user_info
        }
        return Response(data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article.objects.annotate(bookmark_count=Count('bookmarked', distinct=True),comment_count=Count('comments', distinct=True)), pk=article_pk)

    # article = Article.objects.get(pk=article_pk)
    #article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        # comments = Comment.objects.all()
        comments = get_list_or_404(Comment)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, post_pk):
    # article = Article.objects.get(pk=article_pk)
    post = get_object_or_404(Article, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)