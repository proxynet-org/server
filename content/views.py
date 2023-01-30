from django.views.generic import TemplateView
from chartjs.views.columns import BaseColumnsHighChartsView
from django.shortcuts import render
from users.models import User
from .models import Message
