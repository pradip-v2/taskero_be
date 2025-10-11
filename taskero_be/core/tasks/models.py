from django.db import models

from taskero_be.core.models import BaseModel


class TaskStatus(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.pk}-{self.title}"
