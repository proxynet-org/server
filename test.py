import websocket

try:
    ws = websocket.create_connection("ws://localhost:8000/ws/chat/foo/")
    print("WebSocket connection established successfully!")
    ws.send("Hello, World!")
    ws.close()
except ConnectionRefusedError:
    print("WebSocket connection failed.")
