#!/usr/bin/env python3
from django.shortcuts import render 
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomLoginView(LoginView):
    template_name = 'web/login.html'

def login(request):
    return render(request, "web/login.html")

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user
        if user.is_banned():
            ban_days = user.ban_duration
            ban_date = user.ban_date
            ban_until_date = ban_date + timedelta(days=ban_days)
            response_data = {
                'detail': f'User is banned until {ban_until_date}.'
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        token_response = serializer.validated_data
        return Response(token_response, status=status.HTTP_200_OK)