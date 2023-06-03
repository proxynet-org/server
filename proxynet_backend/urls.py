from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from .views import CustomLoginView, login

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),

    # apps
    path('', include('content.urls')),
    path('', include('users.urls')),
    path('', include('zone.urls')),

    # docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # login
    #path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
