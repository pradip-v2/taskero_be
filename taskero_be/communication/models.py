from django.contrib.auth import get_user_model
from django.db import models

from taskero_be.core.models import BaseModel

User = get_user_model()


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


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        db_index=True,
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]


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
