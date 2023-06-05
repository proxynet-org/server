from django.urls import path
from django.contrib.auth.views import LoginView
from .apis import UserViewSet, update_user_location, get_user_info
from . import views

urlpatterns = [
    # apis
    path('api/users/location/', update_user_location, name='update-user-location'),
    path('api/users/register/', UserViewSet.as_view({
        'post': 'create'
    }), name='user-registration'),
    path('api/users/info/', get_user_info, name='get-user-info'),

    # html views
    path("", views.home, name="home"),
    path("privacy/", views.privacy, name="privacy"),
    path("about/", views.about, name="about"),
    path("users/", views.users, name="users"),
    path("users/<int:user_id>/", views.user_details, name="user-details"),
    path("users/<int:user_id>/block/", views.block_user, name="block-user"),
    path("chatrooms/", views.chatrooms, name="chatrooms"),
    path("chatrooms/<int:pk>/", views.chatroom_details, name="chatroom-details"),
    path("general/", views.general_chatroom, name="general"),
    path("general-chat/", views.general_chatroom_details, name="general-chat"),
    path("publications/", views.publications, name="publications"),
    path("publications/<int:pk>/", views.publication_details, name="publication-details"),
    path("chat/", views.chat, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),

    # data views
    path('users/search/', views.search_users, name='search-users'),
]
