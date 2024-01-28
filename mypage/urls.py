from django.urls import path
from . import views

urlpatterns = [
    path('my_info', views.my_info, name='my_info'),
    # path('my_bookmarks', views.my_bookmarks, name='my_bookmarks'),
    # path('my_comments', views.my_comments, name='my_comments'),
    path('my_posts', views.my_posts, name='my_posts'),
    # path('my_test', views.my_test, name='my_test'),
]