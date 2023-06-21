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
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def protect_view(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse("404 Not Found", status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


def chat(request):
    # check user is logged in
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def home(request):
    version = ""
    with open("VERSION", "r") as f:
        version = f.read()
    return render(request, "web/home.html", {"version": version})

def privacy(request):
    return render(request, "web/privacy.html")

def support(request):
    return render(request, "web/support.html")

def about(request):
    return render(request, "web/about.html")

@protect_view
def users(request):
    users = User.objects.all()
    return render(request, "admin/users.html", {"users": users})

@protect_view
def search_users(request):
    query = request.GET.get('q')
    if query:
        # query is either in first name, last name, userHash or email
        users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query) | User.objects.filter(userHash__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        users = User.objects.all()
    user_list = [{'id': user.id, 'email': user.email, 'userHash': user.userHash, "first_name": user.first_name, "last_name":user.last_name, "created_at":user.created_at, "updated_at":user.updated_at} for user in users]
    return JsonResponse({'users': user_list})

@protect_view
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

@protect_view
def block_user(request ,user_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        ban_duration = request.POST.get('ban_duration')  
        definite_ban = request.POST.get('definite_ban')
        unblock = request.POST.get('unblock')
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

@protect_view
def chatrooms(request):
    chatrooms = Chatroom.objects.all()
    return render(request, "admin/chatrooms.html", {"chatrooms": chatrooms})

@protect_view
def chatroom_details(request, pk):
    chatroom = Chatroom.objects.get(id=pk)
    focused_id = request.GET.get('focused_id')
    if focused_id:
        focused_id = int(focused_id)
    chatroom_messages = ChatroomMessages.objects.filter(chatroom=chatroom)
    return render(request, "admin/chatrooms_details.html", {"chatroom": chatroom, "messages": chatroom_messages, "focused_id": focused_id})

@protect_view
def general_chatroom(request):
    messages = Message.objects.all()
    return render(request, "admin/general_chat.html", {"messages": messages})

@protect_view
def general_chatroom_details(request):
    message_list = Message.objects.all()
    focused_message = request.GET.get('focused_message')
    messages = message_list
    if focused_message:
        focused_message = int(focused_message)
        focused_message_coordinates = Message.objects.get(id=focused_message).coordinates
        messages = [message for message in message_list if get_distance_from_two_coordinates(message.coordinates, focused_message_coordinates) < settings.RADIUS_FOR_SEARCH]
    return render(request, "admin/general_chat_details.html", {"messages": messages, "focused_message": focused_message})

@protect_view
def publications(request):
    publications = Publication.objects.all()
    return render(request, "admin/publications.html", {"publications": publications})

@protect_view
def publication_details(request, pk):
    publication = Publication.objects.get(id=pk)
    comments = Comment.objects.filter(Q(publication=publication) & Q(is_reply=False))

    return render(request, "admin/publication_details.html", {"publication": publication, "comments": comments})

def messages_all_view(request):
    user = User.objects.get(id=request.user.id)
    users = []
    all_users = User.objects.all()
    for u in all_users:
        if get_distance_from_two_coordinates(u.coordinates, user.coordinates) < settings.RADIUS_FOR_SEARCH:
            users.append(u)
    if request.method == 'POST':
        message = request.POST.get('message')
        msg = Message.objects.create(user=user, text=message, coordinates=user.coordinates)
    refresh = RefreshToken.for_user(user)
    bearer = str(refresh.access_token)
    messages = Message.objects.all()
    user_messages = []
    websocket_url = settings.WEBSOCKET_URL
    for message in messages:
        if get_distance_from_two_coordinates(message.coordinates, user.coordinates) < settings.RADIUS_FOR_SEARCH:
            user_messages.append(message)
    return render(request, "web-app/messages.html", {"messages": messages, "bearer": bearer, "users":users, "websocket_url": websocket_url})

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.get(email=email)
            if user:
                try:
                    token = PasswordResetTokenGenerator().make_token(user)
                    url = request.build_absolute_uri('/')
                    subject = 'Password Reset'
                    reset_url = url + 'password-reset-confirm?token=' + token + '&uid=' + str(user.id)
                    message = f'Please click the following link to reset your password: {reset_url}'
                    from_email = 'proxynet.dev@gmail.com'
                    recipient_list = [email]
                    message = Mail(
                    from_email='proxynet.dev@gmail.com',
                    to_emails=email,
                    subject='Password Reset',
                    html_content=f'<strong>{message}</strong>')
                    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e)
    return render(request, 'web/password_reset.html', {"message": "Please check your email for the password reset link"})

def password_reset_confirm(request):
    if request.method == 'POST':
        # get token from the query
        try:
            token = request.GET.get('token')
            password = request.POST.get('password')
            user_id = int(request.GET.get('uid'))
            user = User.objects.get(id=user_id)
            if user and PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password)
                user.save()
                return redirect('login')
        except Exception as e:
            print(e)
            return render(request, 'web/password_reset_confirm.html', {"message": "Invalid token"})
    return render(request, 'web/password_reset_confirm.html')