from rest_framework import serializers

from taskero_be.communication.models import Conversation
from taskero_be.communication.models import Message
from taskero_be.communication.models import MessageAttachment
from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.users.api.serializers import UserRelationShortSerializer


class MessageAttachmentRequestSerializer(serializers.Serializer):
    file_url = serializers.CharField()
    key = serializers.CharField()


class MessageAttachmentSerializer(serializers.ModelSerializer[MessageAttachment]):
    class Meta:
        model = MessageAttachment
        fields = serializers.ALL_FIELDS


class MessageSerializer(BaseModelSerializer[Message]):
    sender_data = UserRelationShortSerializer(source="sender", read_only=True)
    attachments = MessageAttachmentRequestSerializer(
        write_only=True,
        many=True,
    )
    attachments_data = MessageAttachmentSerializer(
        many=True,
        source="attachments",
        read_only=True,
    )

    class Meta:
        model = Message
        fields = serializers.ALL_FIELDS


class ConversationSerializer(BaseModelSerializer[Conversation]):
    participants_data = UserRelationShortSerializer(
        many=True,
        source="participants",
        read_only=True,
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = serializers.ALL_FIELDS

    def get_last_message(self, obj):
        message = obj.messages.order_by("-created_at").first()
        return MessageSerializer(message).data if message else None
