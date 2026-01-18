from rest_framework import serializers

from taskero_be.communication.models import Conversation
from taskero_be.communication.models import Message
from taskero_be.communication.models import MessageAttachment
from taskero_be.users.api.serializers import UserRelationShortSerializer


class MessageAttachmentRequestSerializer(serializers.Serializer):
    file_url = serializers.CharField()
    key = serializers.CharField()


class MessageAttachmentSerializer(serializers.ModelSerializer[MessageAttachment]):
    class Meta:
        model = MessageAttachment
        fields = serializers.ALL_FIELDS


class ReplyQuoteSerializer(serializers.Serializer):
    message_id = serializers.CharField()
    content = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer[Message]):
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
    reply_quote = ReplyQuoteSerializer(read_only=True)

    class Meta:
        model = Message
        fields = serializers.ALL_FIELDS


class ConversationSerializer(serializers.ModelSerializer[Conversation]):
    participants_data = UserRelationShortSerializer(
        many=True,
        source="participants",
        read_only=True,
    )
    last_message = MessageSerializer(read_only=True, source="get_last_message")

    class Meta:
        model = Conversation
        fields = serializers.ALL_FIELDS

    def to_representation(self, instance):
        data = super().to_representation(instance)
        message = instance.messages.order_by("-created_at").first()
        data["last_message"] = MessageSerializer(message).data if message else None
        return data


class TwilioCreateCallerIdSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class SendSMSSerializer(serializers.Serializer):
    to = serializers.CharField(required=True)
    sms_body = serializers.CharField(required=True)


class SavedPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    sid = serializers.CharField()


class SavedNumbersResponseSerializer(serializers.Serializer):
    results = SavedPhoneNumberSerializer(many=True)


class VoicemailRecordingSerializer(serializers.Serializer):
    sid = serializers.CharField()
    call_sid = serializers.CharField()
    duration = serializers.IntegerField()
    url = serializers.URLField()
    date_created = serializers.DateTimeField()


class VoicemailRecordingsResponseSerializer(serializers.Serializer):
    recordings = VoicemailRecordingSerializer(many=True)


class ChatHistoryEventSerializer(serializers.Serializer):
    type = serializers.CharField(default="chat.history")
    messages = MessageSerializer(many=True)


class ChatMessageAddReactionEventSerializer(serializers.Serializer):
    type = serializers.CharField(default="message.add_reaction")
    message_id = serializers.CharField()
    reaction = serializers.CharField()


class ChatMessageRemoveReactionEventSerializer(serializers.Serializer):
    type = serializers.CharField(default="message.remove_reaction")
    message_id = serializers.CharField()
    reaction = serializers.CharField()


class ChatMessageCreateMessageEventSerializer(serializers.Serializer):
    type = serializers.CharField(default="message.create_message")
    message = MessageSerializer()


class ChatMessageDeleteMessageEventSerializer(serializers.Serializer):
    type = serializers.CharField(default="message.delete_message")
    message_id = serializers.CharField()


class DummyResponseSerializer(serializers.Serializer):
    chat_event = ChatHistoryEventSerializer()
    message_add_reaction = ChatMessageAddReactionEventSerializer()
    message_remove_reaction = ChatMessageRemoveReactionEventSerializer()
    message_delete_message = ChatMessageDeleteMessageEventSerializer()


class DummyRequestSerializer(serializers.Serializer):
    message_create_message = ChatMessageCreateMessageEventSerializer()
