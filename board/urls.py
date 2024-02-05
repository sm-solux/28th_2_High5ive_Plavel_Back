from django.urls import path
from . import views
#from .views import toggle_bookmark

urlpatterns = [
    # path('home', views.home, name='home'),
    # path('post_list', views.post_list, name='post_list'),    # 최신글
    # path('post_list2', views.post_list2, name='post_list2'), # 인기글

    path('post_filter/', views.post_filter, name='post_filter'),
    #path('post_filter/<str:user_type>/', views.post_filter, name='post_filter'),

    # path('post_create', views.post_create, name='post_create'),
    # path('bookmarked_posts', views.bookmarked_posts, name='bookmarked_posts'),
    # path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),                                
    # path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),                                      # 수정
    # path('post_edit/<int:post_id>/delete_image/<str:image_field>/', views.delete_image, name='delete_image'), # 수정페이지에서 이미지 삭제
    # path('post_delete/<int:post_id>/', views.post_delete, name='post_delete'),
    #path('post/<int:post_id>/bookmark/', toggle_bookmark, name='toggle_bookmark'),
    path('articles/', views.article_list),
    path('articles2/', views.article_list2),
    path('articles/<int:article_pk>/', views.article_detail),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('articles/<int:article_pk>/comments/', views.comment_create),
]