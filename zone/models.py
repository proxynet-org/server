from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from proxynet_backend.proxynet_websocket import ProxynetWebsocket
from users.consumers import ProxynetConsumer
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import json


def chatroom_img_upload_to(instance, filename):
    return "images/chatroom_files/{filename}".format(filename=filename)


class Zone(models.Model):
    coordinates = models.JSONField(blank=True, null=True)
    max_slots = models.IntegerField(blank=True)
    occupied_slots = models.IntegerField(blank=True)


class ChatroomMessages(models.Model):
    chatroom = models.ForeignKey(
        "Chatroom", on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ChatroomMessages, self).save(*args, **kwargs)


class Chatroom(models.Model):
    image = models.ImageField(upload_to=chatroom_img_upload_to, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    current_users = models.ManyToManyField(
        User, related_name="current_users", blank=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner", blank=True, null=True
    )
    # lifetime is how long the chatroom will remain open
    lifetime = models.IntegerField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    messages = models.ManyToManyField(
        ChatroomMessages, related_name="chatroom_messages", blank=True
    )
    coordinates = models.JSONField(blank=True, null=True)


@receiver(post_save, sender=Chatroom)
def send_chatroom_to_websocket(sender, instance, created, **kwargs):
    if created:
        action_type = "post"
    else:
        action_type = "update"
    from zone.serializers import ChatroomSerializer
    from django.conf import settings

    user = instance.owner
    consumer = ProxynetConsumer()
    chatroom_serialized = ChatroomSerializer(instance).data
    base_url = settings.BASE_URL
    try:
        chatroom_serialized["image"] = base_url + instance.image.url
    except:
        chatroom_serialized["image"] = None
    consumer.custom_send_message(
        room_name="chatrooms",
        sender=user.userHash,
        text=chatroom_serialized,
        type="chatroom",
        action_type=action_type,
        coordinates=instance.coordinates,
    )


@receiver(post_delete, sender=Chatroom)
def send_chatroom_deleted_to_websocket(sender, instance, **kwargs):
    from zone.serializers import ChatroomSerializer
    from django.conf import settings

    user = instance.owner
    consumer = ProxynetConsumer()
    chatroom_serialized = ChatroomSerializer(instance).data
    base_url = settings.BASE_URL
    try:
        chatroom_serialized["image"] = base_url + instance.image.url
    except:
        chatroom_serialized["image"] = None
    consumer.custom_send_message(
        room_name="chatrooms",
        sender=user.userHash,
        text=chatroom_serialized,
        type="chatroom",
        action_type="delete",
        coordinates=instance.coordinates,
    )


@receiver(post_save, sender=ChatroomMessages)
def send_chatroom_message_to_websocket(sender, instance, **kwargs):
    from zone.serializers import ChatroomMessagesSerializer

    user = instance.user
    consumer = ProxynetConsumer()
    consumer.custom_send_message(
        room_name=instance.chatroom.name + str(instance.chatroom.id),
        sender=user.userHash,
        text=instance.text,
        type="chatroom_msg",
        action_type="post",
        coordinates=instance.coordinates,
    )