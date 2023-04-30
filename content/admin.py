from django.contrib import admin
from .models import Message, PrivateMessage, Publication

admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(Publication)
