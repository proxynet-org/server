from django.db import models
from django.utils import timezone

# Create your models here.

class Zone(models.Model):
    location = models.CharField(max_length=255, blank=True)
    max_slots = models.IntegerField(blank=True)
    occupied_slots = models.IntegerField(blank=True)