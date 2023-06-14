from users.models import User, UserInRoom
from proxynet_backend.proxynet_websocket import ProxynetWebsocket
import asyncio
import json

me = User.objects.get(id=1)
proxy = ProxynetWebsocket("all")
#proxy.send_message({"type": "message", "sender": me.username, "data": "Hello World", "coordinates": None}, me)

async def main():
    await proxy.send_message(json.dumps({"type": "message", "sender": me.username, "data": "Hello World", "coordinates": None}), me)
asyncio.run(main())

