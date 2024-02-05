from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import Post
from sign.models import CustomUser

User = CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'bio', 'profile_pic', 'user_type', 'gender', 'birth_date'] 

from rest_framework import serializers
from .models import Post, Comment

Article = Post

class ArticleListSerializer(serializers.ModelSerializer):
    #current_user = serializers.SerializerMethodField()  # current_user 필드를 추가합니다.
    bookmark_count = serializers.IntegerField(read_only=True)  # 북마크 수 필드 추가
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 필드 추가
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)  # 작성자 닉네임 필드 추가
    author_type = serializers.CharField(source='author.user_type', read_only=True)  # 작성자 타입 필드 추가

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'bookmark_count', 'comment_count', 'author_nickname', 'author_type', 'created_at')

    # def get_current_user(self, obj):
    #     user = self.context['request'].user
    #     return UserSerializer(user).data 

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)

class ArticleSerializer(serializers.ModelSerializer):
    # comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # author = UserSerializer(allow_null=True)
    author = UserSerializer(allow_null=True, default=User.objects.get_or_create(username='Anonymous')[0])
    comment_set = CommentSerializer(many=True, read_only=True)
    bookmark_count = serializers.IntegerField(read_only=True)  # 북마크 수 필드 추가
    comment_count = serializers.IntegerField(read_only=True)  # 댓글 수 필드 추가

    class Meta:
        model = Article
        fields = '__all__'
