import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from content.utils import get_distance_from_two_coordinates
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from users.models import User, UserInRoom
from django.conf import settings


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware to authenticate WebSocket connections using JWT.
    """

    def __init__(self, inner):
        super().__init__(inner)
        self.authenticator = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        scope["user"] = await self.authenticator.authenticate(scope)
        return await super().__call__(scope, receive, send)


class ProxynetConsumer(WebsocketConsumer):
    def connect(self):
        # Called when the WebSocket is handshaking as part of the connection process.
        # You can override it to set up anything you need for the connection.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()  # Accept the WebSocket connection.

    def disconnect(self, close_code):
        # Called when the WebSocket closes for any reason.
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Called when a WebSocket frame is received.
        data = json.loads(text_data)
        text = data.get("data")
        type = data.get("type")
        coordinates = data.get("coordinates")

        sender_id = self.get_user_id()
        sender = User.objects.get(id=sender_id)

        # Find users within 2km radius
        users = UserInRoom.objects.filter(room=self.room_name)
        self.send_message(sender.username, text, coordinates, type)

    def send_message(self, sender, text, coordinates, type):
        # Send message to a specific user
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": type, "sender": sender, "data": text, "coordinates": coordinates},
        )

    def custom_send_message(self, room_name, sender, text, coordinates, type):
        room_group_name = "chat_%s" % room_name
        if not hasattr(self, "channel_layer"):
            from channels.layers import get_channel_layer

            self.channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_send)(
            room_group_name,
            {"type": type, "sender": sender, "data": text, "coordinates": coordinates},
        )

    def message(self, event):
        self.proxy_event(event)

    def chatroom(self, event):
        self.proxy_event(event)

    def publication(self, event):
        self.proxy_event(event)

    def leave(self, event):
        self.proxy_event(event)

    def join(self, event):
        self.proxy_event(event)

    def proxy_event(self, event):
        sender = event["sender"]
        text = event["data"]
        coordinates = event["coordinates"]
        type = event["type"]

        listener_user_id = self.get_user_id()
        listener_user = User.objects.get(id=listener_user_id)

        if (
            get_distance_from_two_coordinates(coordinates, listener_user.coordinates)
            > settings.RADIUS_FOR_SEARCH
            or listener_user.userHash == sender
        ):
            return

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "data": text,
                    "type": type,
                }
            )
        )

    def get_user_id(self):
        try:
            headers = dict(self.scope["headers"])
            auth = headers.get(b"authorization")
            if auth is None:
                return
            auth = auth.decode("utf-8")
            auth = auth.split(" ")
            auth = auth[1]
            # Get user from JWT
            try:
                validated_token = JWTAuthentication().get_validated_token(auth)
                user_id = validated_token["user_id"]
            except InvalidToken:
                return False
            except TokenError:
                return False
            except Exception as e:
                print(e)
                return False

            return user_id

        except Exception as e:
            print(e)
            return False
