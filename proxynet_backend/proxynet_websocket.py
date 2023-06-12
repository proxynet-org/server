import asyncio
import websockets

class ProxynetWebsocket:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.websocket_server_url = "ws://57.128.39.162:8080/ws/chat/"
        self.websocket_server_url = self.websocket_server_url + self.channel_name + "/"

    async def send_message(self, message):
        try:
            async with websockets.connect(self.websocket_server_url) as websocket:
                await websocket.send(message)
        except Exception as e:
            print("WebSocket connection error:", e)