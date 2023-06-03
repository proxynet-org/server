# path for zone viewset
from django.urls import path
from .apis import ZoneViewSet, ChatroomViewSet

urlpatterns = [
    path('api/zones/', ZoneViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='zone-list'),
    path('api/zones/<int:pk>/', ZoneViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='zone-detail'),
    path('api/chatrooms/', ChatroomViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='chatroom-list'),
    path('api/chatrooms/<int:pk>/', ChatroomViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='chatroom-detail'),
    path('api/chatrooms/<int:pk>/messages/', ChatroomViewSet.as_view({
        'get': 'list_messages',
        'post': 'send_message_to_chatroom'
        }), name='chatroom-messages'),
    path('api/chatrooms/<int:pk>/join/', ChatroomViewSet.as_view({
        'post': 'join_chatroom'
    }), name='chatroom-join'),
    path('api/chatrooms/<int:pk>/leave/', ChatroomViewSet.as_view({
        'post': 'leave_chatroom'
    }), name='chatroom-leave'),
]
