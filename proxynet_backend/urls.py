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
from django.contrib.auth.views import LoginView, LogoutView

from .views import CustomLoginView, login, CustomTokenObtainPairView
from django.views.static import serve 
from django.contrib.admin.views.decorators import staff_member_required
from users.views import protect_view



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
    path('docs/swagger-ui/', protect_view(SpectacularSwaggerView.as_view(template_name="web/swagger.html", url_name='schema')), name='swagger-ui'),
    path('docs/redoc/', protect_view(SpectacularRedocView.as_view(template_name="web/redoc.html", url_name='schema')), name='redoc'),

    # token
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # login
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # media
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
