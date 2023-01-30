from django.db import models

# Create a custom user model with location field
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("First name"), max_length=30, blank=False, null=False)
    last_name = models.CharField(_("Last name"), max_length=30, blank=False, null=False)
    email = models.EmailField(_("Email address"), blank=False, null=False)
    location = models.CharField(_("Location"), blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
