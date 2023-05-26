from django.db import models
from django.utils import timezone

# Create your models here.

class Zone(models.Model):
    coordinates = models.JSONField(blank=True, null=True)
    max_slots = models.IntegerField(blank=True)
    occupied_slots = models.IntegerField(blank=True)