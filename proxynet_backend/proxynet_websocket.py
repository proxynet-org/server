import asyncio
import websockets
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ProxynetWebsocket:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.websocket_server_url = "ws://localhost:8000/ws/chat/"
        self.websocket_server_url = self.websocket_server_url + self.channel_name + "/"

    async def send_message(self, message, sender):
        print("SENDING MESSAGE")
        token = RefreshToken.for_user(sender)
        token = str(token.access_token)
        print("TOKEN: ", token)
        headers = {"Authorization": "Bearer " + token}
        websocket_url = self.websocket_server_url

        async with websockets.connect(websocket_url, extra_headers=headers) as ws:
            await ws.send(message)