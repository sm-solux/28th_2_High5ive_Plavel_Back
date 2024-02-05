from django import urls
from django.urls import path

from . import views
from .views import login, signup

urlpatterns= [
    #path('login', login.as_view()),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    #path('signup', signup.as_view()),

]