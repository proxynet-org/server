# path for message viewset
from django.urls import path
from users import routing
from .apis import MessageViewSet, PrivateMessageViewSet, PublicationViewSet
from django.urls import include

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

    path('api/publications/<int:pk>/like/', PublicationViewSet.as_view({
        'post': 'like'
    }), name='publication-like'),

    path('api/publications/<int:pk>/dislike/', PublicationViewSet.as_view({
        'post': 'dislike'
    }), name='publication-dislike'),

    path('api/publications/<int:pk>/comment/', PublicationViewSet.as_view({
        'post': 'add_comment',
        'get': 'list_comments'
    }), name='publication-comment'),

    path('api/publications/<int:pk>/comment/<int:pkComment>/reply/', PublicationViewSet.as_view({
        'post': 'add_comment_reply',
        'get': 'list_comments_of_comments'
    }), name='publication-comment-reply'),

    path('api/publications/<int:pk>/comment/<int:pkComment>/like/', PublicationViewSet.as_view({
        'post': 'like_comment'
    }), name='publication-comment-like'),

    path('api/publications/<int:pk>/comment/<int:pkComment>/dislike/', PublicationViewSet.as_view({
        'post': 'dislike_comment'
    }), name='publication-comment-dislike'),


    path("", include(routing.websocket_urlpatterns)),

]
