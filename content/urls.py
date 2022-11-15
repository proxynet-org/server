# path for message viewset
from django.urls import path
from .apis import MessageViewSet
from .views import UserListView, UserDetailView
from .views import line_chart, line_chart_json

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
    path('users/', UserListView, name='user-list'),
    path('users/<int:pk>/', UserDetailView, name='user-detail'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]
