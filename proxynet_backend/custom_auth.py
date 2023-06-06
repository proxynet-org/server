from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import Token
from django.utils.translation import gettext_lazy as _
from users.models import User as AuthUser
from users.models import User


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token) -> AuthUser:
        user_id = validated_token.get(api_settings.USER_ID_CLAIM)
        user = User.objects.get(id=user_id)
        if user.is_banned():
            raise InvalidToken(_("user is banned"))

        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        return api_settings.TOKEN_USER_CLASS(validated_token)
