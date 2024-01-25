from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)                                # 작성자
    title = models.CharField(max_length=200)                                                  # 제목
    content = models.TextField()                                                              # 내용
    #image = models.ImageField(upload_to='post_images/', null=True, blank=True)               # 이미지 첨부
    bookmarked = models.ManyToManyField(User, related_name='bookmarked_posts', blank=True) # 북마크
    created_at = models.DateTimeField(auto_now_add=True)                                      # 작성일
    updated_at = models.DateTimeField(auto_now=True)                                          # 수정일


    class Meta:
        # 최신 게시글이 위에 오도록
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

    class Meta:
        ordering = ['created_at']