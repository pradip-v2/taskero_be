from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from taskero_be.core.models import BaseModel

User = get_user_model()

PRIVATE_CONVERSATION_PARTICIPANT_COUNT = 2


class Conversation(BaseModel):
    class ConversationType(models.TextChoices):
        PRIVATE = "private", "Private"
        GROUP = "group", "Group"

    name = models.CharField(max_length=255, blank=True, default="")
    type = models.CharField(
        max_length=10,
        choices=ConversationType.choices,
        default=ConversationType.PRIVATE,
    )
    participants = models.ManyToManyField(
        User,
        related_name="conversations",
    )

    def __str__(self):
        return (
            self.name
            or f"{self.type} chat ({','.join([participant.name for participant in self.participants.all()])})"  # noqa: E501
        )

    def validate_private_conversation(self):
        if self.type == Conversation.ConversationType.PRIVATE:
            if self.participants.count() != PRIVATE_CONVERSATION_PARTICIPANT_COUNT:
                msg = "Private conversation must have exactly 2 participants."
                raise ValidationError(msg)


class Message(BaseModel):
    class MessageType(models.TextChoices):
        TEXT = "text", "Text"
        AUDIO = "audio", "Audio"
        FILE = "file", "File"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    reply_to = models.JSONField(blank=True, default=dict, null=True)
    message_type = models.CharField(
        max_length=10,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )
    mentioned_users = models.ManyToManyField(
        User,
        related_name="mentioned_in",
        blank=True,
    )
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    reactions = models.JSONField(null=True, default=dict)

    class Meta:
        ordering = ["-id"]

    def to_dict(self):
        return {
            "id": self.id,
            "conversation": self.conversation_id,
            "sender": self.sender_id,
            "content": self.content,
            "reply_to": self.reply_to,
            "message_type": self.message_type,
            "mentioned_users": list(self.mentioned_users.values_list("id", flat=True)),
            "is_read": self.is_read,
            "is_edited": self.is_edited,
            "is_starred": self.is_starred,
            "reactions": self.reactions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "sender_data": {
                "id": self.sender.id,
                "first_name": self.sender.name,
                "last_name": self.sender.name,
                "email": self.sender.email,
                "profile_picture": None,
            }
            if self.sender
            else None,
            "attachments_data": [
                {
                    "id": att.id,
                    "message": att.message_id,
                    "file_url": att.file_url,
                    "key": att.key,
                }
                for att in self.attachments.all()
            ],
            "reply_quote": self.reply_to if self.reply_to else None,
        }


class MessageAttachment(models.Model):
    message = models.ForeignKey[Message](
        Message,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    file_url = models.URLField()
    key = models.CharField(max_length=512)  # S3 object key

    def __str__(self):
        return f"{self.pk}-Attachment for Message ID {self.message.pk}"
