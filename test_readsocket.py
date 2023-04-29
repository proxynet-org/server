import websocket

def on_message(ws, message):
    print("Received '%s'" % message)

try:
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/chat/test/", on_message=on_message)
    print("WebSocket connection established successfully!")
    ws.run_forever()
except ConnectionRefusedError:
    print("WebSocket connection failed.")
