import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django_tenants.utils import schema_context

from taskero_be.communication.models import Message
from taskero_be.communication.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send initial message history
        messages = await self.get_last_messages(self.conversation_id)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat.history",
                    "messages": messages,
                },
            ),
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = await self.create_message(data)
        serialized = await self.serialize_message(message)

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat.message", "message": serialized},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def get_last_messages(self, conversation_id, limit=30):
        with schema_context(self.scope["schema_name"]):
            messages = Message.objects.filter(conversation_id=conversation_id).order_by(
                "-created_at",
            )[:limit]
            return MessageSerializer(messages, many=True).data[::-1]

    @database_sync_to_async
    def create_message(self, data):
        with schema_context(self.scope["schema_name"]):
            return Message.objects.create(
                conversation_id=self.conversation_id,
                sender=self.scope["user"],
                content=data["message"],
            )

    @database_sync_to_async
    def serialize_message(self, message):
        return MessageSerializer(message).data
