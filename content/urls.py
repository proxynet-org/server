# path for message viewset
from django.urls import path
from .apis import MessageViewSet, PrivateMessageViewSet, PublicationViewSet

urlpatterns = [
    path('api/messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='message-list'),
    path('api/messages/<int:pk>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='message-detail'),

    path('api/send-private-messages/', PrivateMessageViewSet.as_view({
        'post': 'create'
    }), name='private-message-create'),
    path('api/view-convo-with-receiver/<int:pk>/', PrivateMessageViewSet.as_view({
        'get': 'view_convo_with_receiver'
    }), name='private-message-view-convo-with-receiver'),

    path('api/publications/', PublicationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='publication-list'),

    path('api/publications/<int:pk>/', PublicationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='publication-detail'),

]
