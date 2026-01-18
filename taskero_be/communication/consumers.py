import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django_tenants.utils import schema_context

from taskero_be.communication.models import Message
from taskero_be.communication.models import MessageAttachment
from taskero_be.core.s3_utils import remove_temp_tag_from_s3_object


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
        if data["type"] == "message.add_reaction":
            reactions = await self.add_reaction(data)
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "message.reactions", "message_reactions": reactions},
            )
        elif data["type"] == "message.remove_reaction":
            reactions = await self.remove_reaction(data)
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "message.reactions", "message_reactions": reactions},
            )
        elif data["type"] == "message.create_message":
            message = await self.create_message(data)
            serialized = await self.serialize_message(message)

            await self.channel_layer.group_send(
                self.group_name,
                {"type": "chat.message", "message": serialized},
            )
        elif data["type"] == "message.delete_message":
            await self.delete_message(data)
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "chat.message_deleted", "message_id": data["message_id"]},
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def chat_message_deleted(self, event):
        event["type"] = "chat.message_deleted"
        await self.send(text_data=json.dumps(event))

    async def message_reactions(self, event):
        event["message_reactions"]["type"] = "message.reactions"
        await self.send(text_data=json.dumps(event["message_reactions"]))

    @database_sync_to_async
    def add_reaction(self, data):
        with schema_context(self.scope["schema_name"]):
            message = Message.objects.get(id=data["message_id"])
            message_reaction = message.reactions or {}

            message_reaction[data["reaction"]] = message_reaction.get(
                data["reaction"],
                {},
            )
            message_reaction[data["reaction"]][str(self.scope["user"].id)] = True
            message.reactions = message_reaction
            message.save()
            return {"message_id": message.id, "reactions": message.reactions}

    @database_sync_to_async
    def remove_reaction(self, data):
        with schema_context(self.scope["schema_name"]):
            message = Message.objects.get(id=data["message_id"])
            message_reaction = message.reactions or {}
            message_reaction[data["reaction"]].pop(str(self.scope["user"].id), None)
            message.reactions = message_reaction
            message.save()
            return {"message_id": message.id, "reactions": message.reactions}

    @database_sync_to_async
    def get_last_messages(self, conversation_id, limit=30):
        with schema_context(self.scope["schema_name"]):
            messages = Message.objects.filter(conversation_id=conversation_id).order_by(
                "-id",
            )[:limit]
            return [message.to_dict() for message in messages]

    @database_sync_to_async
    def create_message(self, data):
        with schema_context(self.scope["schema_name"]):
            message = Message.objects.create(
                conversation_id=self.conversation_id,
                sender=self.scope["user"],
                content=data["message"],
                reply_to=data.get("reply_to", None),
            )

            attachments = data.get("attachments", [])
            for att in attachments:
                # Remove temp tag from S3 file now that it's in use
                updated_key, updated_url = remove_temp_tag_from_s3_object(att["key"])
                # Optionally create MessageAttachment records if your model supports it
                MessageAttachment.objects.create(
                    message=message,
                    file_url=updated_url,
                    key=updated_key,
                )

            return message

    @database_sync_to_async
    def delete_message(self, data):
        with schema_context(self.scope["schema_name"]):
            message = Message.objects.get(id=data["message_id"])
            message.delete()
            return True

    @database_sync_to_async
    def serialize_message(self, message):
        with schema_context(self.scope["schema_name"]):
            return message.to_dict()
