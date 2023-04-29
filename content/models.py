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

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField()
    location = models.CharField(max_length=255, blank=True)
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
    text = models.TextField()
    image = models.ImageField(upload_to='publications', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='publications', blank=True, null=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            if self.image:
                self.image = self.compressImage(self.image)
        self.updated_at = timezone.now()
        return super(Publication, self).save(*args, **kwargs)
    def compressImage(self, image:models.ImageField):
        # compress image
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile
        import sys
        import os

        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image
