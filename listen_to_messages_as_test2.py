import requests
import websocket
import json

# Login to obtain JWT token
login_url = "http://localhost:8000/api/token/"  # Replace with your login URL
username = "test2"  # Replace with your username
password = "porus"  # Replace with your password

login_data = {"username": username, "password": password}

response = requests.post(login_url, data=login_data)

if response.status_code == 200:
    jwt_token = response.json().get("access")
    print("Login successful. JWT token obtained.")
else:
    print("Login failed.")
    exit()

# WebSocket connection details
websocket_url = "ws://localhost:8000/ws/chat/all/?token=" + jwt_token

# Add JWT token to the request headers
headers = {"Authorization": f"Bearer {jwt_token}"}

# Establish WebSocket connection and send message
ws = websocket.WebSocket()
ws.connect(websocket_url)

# Receive and print the response from the WebSocket server
print("Listening for messages:")
while True:
    response = ws.recv()
    print("Response:", response)

# Close the WebSocket connection
ws.close()
