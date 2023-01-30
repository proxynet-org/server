# path for message viewset
from django.urls import path
from .apis import MessageViewSet

urlpatterns = [
    path('api/messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='message-list'),
    path('api/messages/<int:pk>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='message-detail')
]
