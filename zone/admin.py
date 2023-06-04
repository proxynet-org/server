from django.contrib import admin
from .models import Zone, Chatroom, ChatroomMessages

# Register your models here.

admin.site.register(Zone)
admin.site.register(Chatroom)
admin.site.register(ChatroomMessages)

