# path for message viewset
from django.urls import path
from .apis import MessageViewSet
from .views import UserListView, UserDetailView

urlpatterns = [
    path('messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='message-list'),
    path('messages/<int:pk>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='message-detail'),
    path('users/', UserListView, name='user-list'),
    path('users/<int:pk>/', UserDetailView, name='user-detail'),
]
