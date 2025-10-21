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
            or f"{self.type} chat ({','.join([participant.name for participant in self.participants.all()])})"
        )


class Message(BaseModel):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
