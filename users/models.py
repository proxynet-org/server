import os
from django.db import models
from binascii import hexlify

# Create a custom user model with location field
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    def _createHash():
        return hexlify(os.urandom(16))
    userHash = models.CharField(max_length=32, default=_createHash, unique=True, null=True)
    first_name = models.CharField(_("First name"), max_length=30, blank=False, null=False)
    last_name = models.CharField(_("Last name"), max_length=30, blank=False, null=False)
    email = models.EmailField(_("Email address"), blank=False, null=False)
    coordinates = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username

