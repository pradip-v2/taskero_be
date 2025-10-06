from django.db import models

from taskero_be.core.models import BaseModel
from taskero_be.projects.models import Project


class Task(BaseModel):
    title = models.CharField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        db_index=True,
    )
    description = models.TextField(blank=True, default="")
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )
    level = models.PositiveIntegerField(default=1, db_index=True)
