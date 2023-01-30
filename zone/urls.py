# path for zone viewset
from django.urls import path
from .apis import ZoneViewSet

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
]
