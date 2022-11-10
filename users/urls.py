from .apis import update_location
from django.urls import path


urlpatterns = [
    path('api/users/location/', update_location, name='user-update-location'),
]
