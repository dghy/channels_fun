# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from chat.models import Message, ChatGroup


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % str(self.room_name)

        # Join room group
        # self.channel_layer -> redis channel_layer
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        user = get_object_or_404(User, id=user_id)
        if not user_id.isdigit():
            raise Http404

        chat_group = get_object_or_404(ChatGroup, id=self.room_name)
        # save message in the DB
        message_object = Message.objects.create(text=message,
                                                user=user,
                                                group=chat_group)

        # Send message to room group, generates event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'date': str(message_object.published.strftime('%y-%m-%d %H:%M:%S')),
                'user': user.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        # this will be available in the 'data' key of MessageEvent
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'date': event['date']
        }))
