from django.shortcuts import render
from content.models import Message, Publication, Comment, PrivateMessage
from django.db.models import Q
from zone.models import Chatroom, ChatroomMessages
from content.utils import get_distance_from_two_coordinates
from django.shortcuts import redirect
from .models import User
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings




def chat(request):
    # check user is logged in
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def home(request):
    return render(request, "web/home.html")

def privacy(request):
    return render(request, "web/privacy.html")

def support(request):
    return render(request, "web/support.html")

def about(request):
    return render(request, "web/about.html")

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
    messages = Message.objects.filter(user=user)
    # Get all chatroomMessages from the user, and take only the chatrooms that have messages from the user
    user_chatroom_messages = ChatroomMessages.objects.filter(user=user)
    # get distinct chatrooms from the user_chatroom_messages
    chatrooms_of_user_id = user_chatroom_messages.values('chatroom').distinct()
    chatrooms_of_user = Chatroom.objects.filter(id__in=chatrooms_of_user_id)

    private_messages = PrivateMessage.objects.filter(sender=user)
    is_banned = user.is_banned()
    ban_definite = user.ban_duration == -1
    ban_duration = timedelta(days=user.ban_duration)  # Assuming user.ban_duration is the ban duration in days
    ban_until_date = timezone.now() + ban_duration
    ban_until_date_str = ban_until_date.strftime("%d %B %Y")
    return render(request, "admin/user_details.html", {"user": user, "messages": messages, "chatrooms": chatrooms_of_user, "private_messages":private_messages, "is_banned": is_banned, "ban_date": ban_until_date_str, "ban_definite": ban_definite})

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

def chatrooms(request):
    chatrooms = Chatroom.objects.all()
    print(chatrooms)
    return render(request, "admin/chatrooms.html", {"chatrooms": chatrooms})

def chatroom_details(request, pk):
    chatroom = Chatroom.objects.get(id=pk)
    focused_id = request.GET.get('focused_id')
    if focused_id:
        focused_id = int(focused_id)
    chatroom_messages = ChatroomMessages.objects.filter(chatroom=chatroom)
    return render(request, "admin/chatrooms_details.html", {"chatroom": chatroom, "messages": chatroom_messages, "focused_id": focused_id})

def general_chatroom(request):
    messages = Message.objects.all()
    return render(request, "admin/general_chat.html", {"messages": messages})

def general_chatroom_details(request):
    message_list = Message.objects.all()
    focused_message = request.GET.get('focused_message')
    messages = message_list
    if focused_message:
        focused_message = int(focused_message)
        focused_message_coordinates = Message.objects.get(id=focused_message).coordinates
        messages = [message for message in message_list if get_distance_from_two_coordinates(message.coordinates, focused_message_coordinates) < settings.RADIUS_FOR_SEARCH]
    return render(request, "admin/general_chat_details.html", {"messages": messages, "focused_message": focused_message})

def publications(request):
    publications = Publication.objects.all()
    return render(request, "admin/publications.html", {"publications": publications})

def publication_details(request, pk):
    publication = Publication.objects.get(id=pk)
    comments = Comment.objects.filter(Q(publication=publication) & Q(is_reply=False))

    return render(request, "admin/publication_details.html", {"publication": publication, "comments": comments})