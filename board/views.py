from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models import Count
from .forms import CommentForm, PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import datetime

# 글 보기 페이지
@login_required  # 로그인한 상태여야 조회 가능
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 현재 날짜를 얻습니다.
    today = datetime.date.today()
    # 생년월일이 있는 경우 나이를 계산합니다.
    if post.author.birth_date:
        # 나이 계산 로직
        age = today.year - post.author.birth_date.year + 1
    else:
        age = None

    bookmarks_count = post.bookmarked.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # 현재 로그인한 사용자
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()

    # render 함수에 추가적으로 나이 정보를 context에 담아 전달합니다.
    context = {
        'post': post,
        'form': form,
        'age': age,
        'bookmarks_count': bookmarks_count,
    }
    
    return render(request, 'post_detail.html', context)


# # 댓글 수 세기 -> 최적화엔 더 좋은데 코드 수정 필요.
# def post_list(request):
#     # annotate()를 사용하여 각 게시글에 대한 댓글 수를 미리 계산
#     post_list = Post.objects.annotate(comments_count=Count('comments'))
#     return render(request, 'post_list.html', {'post_list': post_list})


# 글 목록1 (최신글)
def post_list(request):
    posts = Post.objects.order_by('-created_at').annotate(bookmark_count=Count('bookmarked'))

    # 현재 로그인한 사용자를 context에 추가합니다.
    current_user = request.user
    if current_user.is_authenticated:
        # 로그인한 상태라면, 현재 사용자의 정보를 context에 추가합니다.
        context = {
            'posts': posts,
            'current_user_nickname': current_user.nickname,
            'current_user_profile_pic': current_user.profile_pic.url if current_user.profile_pic else None,
            'current_user_user_type': current_user.user_type,
        }
    else:
        # 로그인하지 않은 상태라면, 사용자 정보를 비워둡니다.
        context = {
            'posts': posts,
            'current_user_nickname': None,
            'current_user_profile_pic': None,
            'current_user_user_type': None,
        }

    return render(request, 'post_list.html', context)


# 글 목록2 (인기글)
def post_list2(request):
    posts = Post.objects.annotate(
        bookmark_count=Count('bookmarked', distinct=True),
        comments_count=Count('comments')
    ).order_by('-bookmark_count', '-comments_count')
    return render(request, 'post_list2.html', {'posts': posts})


# 글 작성
@login_required # 로그인한 상태에서만 게시글 작성 가능
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인한 사용자를 author로 설정
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


# 수정
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return HttpResponseForbidden()  # 작성자가 아니면 403 Forbidden 응답을 반환합니다.
    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', post.id)
    return render(request, 'post_edit.html', {'post': post})

# 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return HttpResponseForbidden()  # 작성자가 아니면 403 Forbidden 응답을 반환합니다.
    post.delete()
    return redirect('post_list')

# 북마크 기능
@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.bookmarked.all():
        post.bookmarked.remove(request.user)
    else:
        post.bookmarked.add(request.user)
    return redirect('post_detail', post_id=post_id)

# 북마크된 글
@login_required
def bookmarked_posts(request):
    user = request.user
    bookmarks = user.bookmarked_posts.all()

    for post in bookmarks:
        post.bookmarks_count = post.bookmarked.count()

    return render(request, 'bookmarked_posts.html', {'bookmarks': bookmarks})