from django.urls import path
from django.contrib.auth.views import LoginView
from .apis import UserViewSet, update_user_location

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('api/users/location/', update_user_location, name='update-user-location'),
    path('api/users/register/', UserViewSet.as_view({
        'post': 'create'
    }), name='user-registration'),
]
