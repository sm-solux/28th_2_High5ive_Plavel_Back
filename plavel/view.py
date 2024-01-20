from django.shortcuts import render,redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def home(request):
    return render(request,'home.html')
