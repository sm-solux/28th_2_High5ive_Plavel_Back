from django.urls import path
from . import views

urlpatterns = [
    path('post_list', views.post_list, name='post_list'),
    path('post_create', views.post_create, name='post_create'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post_edit/<int:post_id>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:post_id>/', views.post_delete, name='post_delete'),
]