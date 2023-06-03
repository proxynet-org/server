from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


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

def user_details(request, user_id):
    user = User.objects.get(id=user_id)
    messages = []
    chatrooms = []
    friends = []
    is_banned = user.is_banned()
    ban_definite = user.ban_duration == -1
    ban_duration = timedelta(days=user.ban_duration)  # Assuming user.ban_duration is the ban duration in days
    ban_until_date = timezone.now() + ban_duration
    ban_until_date_str = ban_until_date.strftime("%d %B %Y")
    return render(request, "admin/user_details.html", {"user": user, "messages": messages, "chatrooms": chatrooms, "friends": friends, "is_banned": is_banned, "ban_date": ban_until_date_str, "ban_definite": ban_definite})

def block_user(request ,user_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        ban_duration = request.POST.get('ban_duration')  
        definite_ban = request.POST.get('definite_ban')
        unblock = request.POST.get('unblock')
        print("unblock", unblock)
        print("definite_ban", definite_ban) 
        print("ban_duration", ban_duration)
        if unblock == "true":
            user.ban_duration = 0
            user.ban_date = None
            user.save()
        elif definite_ban == "true":
            user.ban_duration = -1
            user.ban_date = None
            user.save()
        else:
            ban_duration = int(ban_duration)
            user.ban_duration = ban_duration
            user.ban_date = timezone.now()
            user.save()
        return redirect('user-details', user_id=user_id) 