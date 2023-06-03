from django.shortcuts import render
from .models import User
from django.http import JsonResponse

def chat(request):
    # check user is logged in
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def home(request):
    return render(request, "web/home.html")

def users(request):
    users = User.objects.all()
    return render(request, "admin/users.html", {"users": users})

def search_users(request):
    query = request.GET.get('q')
    if query:
        # query is either in first name, last name, userHash or email
        users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query) | User.objects.filter(userHash__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        users = User.objects.all()
    user_list = [{'id': user.id, 'email': user.email, 'userHash': user.userHash, "first_name": user.first_name, "last_name":user.last_name, "created_at":user.created_at, "updated_at":user.updated_at} for user in users]
    return JsonResponse({'users': user_list})

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "web/home.html", {"user": user})