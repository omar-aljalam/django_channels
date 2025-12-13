from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        message = json.loads(text_data).get("message", "")
        print(f"Received message: {message}")
    
    def receiver(self, text_data):
        pass
 