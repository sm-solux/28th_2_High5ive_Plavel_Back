# from django import urls
# from django.urls import path

# from . import views
# from .views import login, signup

# urlpatterns= [
#     path('login', login.as_view()),
#     path('logout', views.logout, name="logout"),
#     path('login', views.login, name="login"),
#     path('signup', views.signup, name="signup"),
#     #path('signup', signup.as_view()),

# ]

from django.urls import path, include
from .views import RegistrationAPI, LoginAPI, UserAPI

urlpatterns = [
    path("signup", RegistrationAPI.as_view()),
    path("login", LoginAPI.as_view()),
    path("user", UserAPI.as_view()),
]