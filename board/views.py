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