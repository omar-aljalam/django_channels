from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import Message
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["id"]
        if not user.is_authenticated:
            self.close()
            return
        
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get("message")

        if not message_text:
            return
        Message.objects.create(
            sender=self.scope["user"],
            receiver=User.objects.get(id=self.receiver_id),
            message=message_text,
        )