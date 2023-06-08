from django.contrib import admin
from .models import Message, PrivateMessage, Publication, Comment

admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.register(Publication)
admin.site.register(Comment)
