from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_swagger_view(title='Proxynet API')

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),

    # apps
    path('', include('content.urls')),
    path('', include('users.urls')),
    path('', include('zone.urls')),

    # docs
    url(r'^docs/', schema_view),

    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
