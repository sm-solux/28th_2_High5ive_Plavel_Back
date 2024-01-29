from django.urls import path
from . import views
from .views import toggle_bookmark

urlpatterns = [
    path('home', views.home, name='home'),
    path('post_list', views.post_list, name='post_list'),
    path('post_list2', views.post_list2, name='post_list2'),
    path('post_create', views.post_create, name='post_create'),
    path('bookmarked_posts', views.bookmarked_posts, name='bookmarked_posts'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/bookmark/', toggle_bookmark, name='toggle_bookmark'),
]