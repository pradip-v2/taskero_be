from django.db import models

from taskero_be.core.models import BaseModel


class TaskStatus(BaseModel):
    title = models.CharField(max_length=128)
    parent_status = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="children",
    )

    def __str__(self):
        return f"{self.pk}-{self.title}"
