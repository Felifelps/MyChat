import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from users.models import User
from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["users"]
        self.room_group_name = f"chat_{self.room_name}"

        self.users = [User.objects.get(username=username) for username in self.room_name.split('_')]
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        sender_username = text_data_json['username']

        receiver_username = self.room_name.replace(sender_username, '').replace('_', '')

        message = Message(
            sender=User.objects.get(username=sender_username),
            receiver=User.objects.get(username=receiver_username),
            text=text_data_json['message']
        )
        message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message", 
                "date": message.date.strftime("%d/%m/%Y %H:%M"),
                **text_data_json
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        event.pop('type')

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
