from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Message, self).save(*args, **kwargs)

    def distance_from_two_locations(location1, location2):
        """
        returns the distance in km
        location is a string in the format of "lat,lng"
        """
        from geopy.distance import geodesic

        lat1, lng1 = location1.split(",")
        lat2, lng2 = location2.split(",")
        return geodesic((lat1, lng1), (lat2, lng2)).km
