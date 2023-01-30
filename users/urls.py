from django.urls import path
from django.contrib.auth.views import LoginView
from .apis import UserViewSet

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('api/users/register/', UserViewSet.as_view({
        'post': 'create'
    }), name='user-registration'),
]
