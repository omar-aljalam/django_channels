from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            "message": "WebSocket connection established.",
            "status": "connected"
        }))

        async_to_sync(self.channel_layer.group_add)(
            "chat_group",
            self.channel_name
        )

    def receive(self, text_data):
        message = json.loads(text_data).get("message", "")
        print(f"Received message: {message}")
    
    def disconnect(self, code):
        print(f"WebSocket disconnected with code: {code}")
