from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.db.models import Count
from .forms import CommentForm, PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# 글 보기(조회)
@login_required # 로그인한 상태여야 조회 가능
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user # 현재 로그인한 사용자
            comment.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     return render(request, 'post_detail.html', {'post': post})

# 글 목록
def post_list(request):
    # posts = Post.objects.all()
    posts = Post.objects.annotate(bookmark_count=Count('bookmarked'))
    return render(request, 'post_list.html', {'posts': posts})

# # 댓글 수 세기 -> 최적화엔 더 좋은데 추후 코드 수정 필요.
# def post_list(request):
#     # annotate()를 사용하여 각 게시글에 대한 댓글 수를 미리 계산
#     post_list = Post.objects.annotate(comments_count=Count('comments'))
#     return render(request, 'post_list.html', {'post_list': post_list})

# 글 작성
@login_required # 로그인한 상태에서만 게시글 작성 가능
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인한 사용자를 author로 설정
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

# def post_create(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         post = Post.objects.create(title=title, content=content)
#         return redirect('post_detail', post.id)
#     return render(request, 'post_create.html')

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
    return render(request, 'bookmarked_posts.html', {'bookmarks': bookmarks})