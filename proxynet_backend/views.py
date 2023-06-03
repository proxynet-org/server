#!/usr/bin/env python3
from django.shortcuts import render 
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'web/login.html'

def login(request):
    return render(request, "web/login.html")