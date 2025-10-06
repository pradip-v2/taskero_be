from django.db import models

from taskero_be.core.models import BaseModel
from taskero_be.users.models import User


class Project(BaseModel):
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        related_name="projects",
    )
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.pk}-{self.title}"
