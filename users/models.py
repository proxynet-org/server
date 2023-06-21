import os
from django.db import models
import random

# Create a custom user model with location field
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import random
import string


def createRandomString():
    hash = "".join(random.choice(string.ascii_lowercase) for i in range(6))
    while User.objects.filter(userHash=hash).exists():
        hash = "".join(random.choice(string.ascii_lowercase) for i in range(6))
    return str(hash)


def _generate_random_color():
    while True:
        # generate random rgb values
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # calculate the perceived brightness of the color
        brightness = (r * 299 + g * 587 + b * 114) / 1000

        # check if the color is readable on a white background
        if brightness > 125:
            return f"#{r:02x}{g:02x}{b:02x}"


class User(AbstractUser):
    def _createHash():
        return createRandomString()

    def generate_random_color():
        return _generate_random_color()

    userHash = models.CharField(max_length=32, default=createRandomString, unique=True)
    random_color = models.CharField(max_length=7, default=generate_random_color)
    first_name = models.CharField(
        _("First name"), max_length=30, blank=False, null=False
    )
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
        self.random_color = _generate_random_color()
        self.save()


class UserInRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.TextField(max_length=100, blank=False, null=False)
