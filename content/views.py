from django.shortcuts import render
from users.models import User
from .models import Message

# Render users.html


def UserListView(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'content/users.html', context)


def UserDetailView(request, pk):
    context = {
        'messages': Message.objects.filter(user=pk),
    }
    return render(request, 'content/user_messages.html', context)
