from django.db import models
from django.utils import timezone
from users.models import User
from content.models import Message

def chatroom_img_upload_to(instance, filename):
    return 'images/chatroom_files/{filename}'.format(filename=filename)

class Zone(models.Model):
    coordinates = models.JSONField(blank=True, null=True)
    max_slots = models.IntegerField(blank=True)
    occupied_slots = models.IntegerField(blank=True)


class ChatroomMessage(Message):
    chatroom = models.ForeignKey('Chatroom', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ChatroomMessage, self).save(*args, **kwargs)


class Chatroom(models.Model):
    image = models.ImageField(upload_to=chatroom_img_upload_to, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    current_users = models.ManyToManyField(User, related_name='current_users', blank=True)
    # lifetime is how long the chatroom will remain open
    lifetime = models.IntegerField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    messages = models.ManyToManyField(ChatroomMessage, related_name='messages', blank=True)
    coordinates = models.JSONField(blank=True, null=True)
    
