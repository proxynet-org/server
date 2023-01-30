from .apis import update_location
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('api/users/location/', update_location, name='user-update-location'),
    path("login/", LoginView.as_view(), name="login"),
]
