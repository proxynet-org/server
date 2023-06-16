from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from proxynet_backend.proxynet_websocket import ProxynetWebsocket
from users.consumers import ProxynetConsumer
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.dispatch import receiver
from django.db.models.signals import post_save
import json

# Create your models here.

def publications_img_upload_to(instance, filename):
    return 'images/publications_files/{filename}'.format(filename=filename)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Message, self).save(*args, **kwargs)

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.text}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(PrivateMessage, self).save(*args, **kwargs)
    
class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=publications_img_upload_to, blank=True, null=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Publication, self).save(*args, **kwargs)

class Comment(models.Model):
    is_reply = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.publication}: {self.text}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

@receiver(post_save, sender=Message)
def send_message_to_websocket(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        consumer = ProxynetConsumer()
        message = instance.text
        consumer.custom_send_message(room_name="all", sender=user.userHash, text=message, type="message", coordinates=instance.coordinates)


@receiver(post_save, sender=Publication)
def send_publication_to_websocket(sender, instance, created, **kwargs):
    if created:
        from content.serializers import PublicationSerializer
        from django.conf import settings
        user = instance.user
        consumer = ProxynetConsumer()
        publication_serialized = PublicationSerializer(instance).data
        base_url = settings.BASE_URL
        publication_serialized['image'] = base_url + publication_serialized['image']
        consumer.custom_send_message(room_name="all", sender=user.userHash, text=publication_serialized, type="publication", coordinates=instance.coordinates)