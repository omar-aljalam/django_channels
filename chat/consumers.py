from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            "message": "WebSocket connection established.",
            "status": "connected"
        }))

    def receive(self, text_data):
        message = json.loads(text_data).get("message", "")
        print(f"Received message: {message}")
    
    def disconnect(self, code):
        print(f"WebSocket disconnected with code: {code}")
