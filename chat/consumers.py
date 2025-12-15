from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import Message, UserChannel
import json
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["id"]

        if not user.is_authenticated:
            self.close()
            return

        try:
            user_channel = UserChannel.objects.get(
                user=user
            )
            user_channel.channel_name = self.channel_name
            user_channel.save()
        except UserChannel.DoesNotExist:
            UserChannel.objects.create(
                user=user,
                channel_name=self.channel_name
            )
        self.accept()

    def receive(self, text_data):
        load_data = json.loads(text_data)
        message_text = load_data.get("message")

        if not message_text:
            return
        Message.objects.create(
            sender=self.scope["user"],
            receiver=User.objects.get(id=self.receiver_id),
            message=message_text,
        )
        try:
            receiver_channel = UserChannel.objects.get(
                user=User.objects.get(id=self.receiver_id))
            data = {
                "type": "chat_message",
                "sender": self.scope["user"].id,
                "receiver": self.receiver_id,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": message_text
            }

            async_to_sync(self.channel_layer.send)(
                receiver_channel.channel_name, data)
        except UserChannel.DoesNotExist:
            pass

    def chat_message(self, event):
        data = json.dumps(event)
        self.send(data)
