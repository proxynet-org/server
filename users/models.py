import os
from django.db import models

# Create a custom user model with location field
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import random
import string


def createRandomString():
    hash = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    while User.objects.filter(userHash=hash).exists():
        hash  = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
    return str(hash) 

class User(AbstractUser):
    def _createHash():
        return createRandomString()
    userHash = models.CharField(max_length=32, default=createRandomString, unique=True)
    first_name = models.CharField(_("First name"), max_length=30, blank=False, null=False)
    last_name = models.CharField(_("Last name"), max_length=30, blank=False, null=False)
    email = models.EmailField(_("Email address"), blank=False, null=False)
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_in_chatroom = models.BooleanField(default=False)
    ban_duration = models.IntegerField(default=0)
    ban_date = models.DateTimeField(null=True, blank=True)

    def is_banned(self):
        if self.ban_duration == -1:
            return True
        if self.ban_duration == 0:
            return False
        else:
            if self.ban_date is not None:
                day_since_ban = (timezone.now() - self.ban_date).days
                if day_since_ban > self.ban_duration:
                    self.ban_duration = 0
                    self.ban_date = None
                    self.save()
                    return False
                else:
                    return True
            else:
                return False

    def delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)


    def __str__(self):
        return self.username

    def change_user_hash(self):
        string = createRandomString()
        self.userHash = string
        self.save()
    



class UserInRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.TextField(max_length=100, blank=False, null=False)