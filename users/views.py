from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def custom_login(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to the desired page
        return redirect('home')
    else:
        # Render the custom login template
        return render(request, 'login.html')

def chat(request):
    # check user is logged in
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def home(request):
    return render(request, "web/home.html")

def login(request):
    return render(request, "web/login.html")