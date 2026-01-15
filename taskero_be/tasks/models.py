from django.db import models
from django.db import transaction

from taskero_be.core.models import BaseModel
from taskero_be.core.tasks.models import TaskStatus
from taskero_be.projects.models import Project
from taskero_be.users.models import User


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
        related_name="subtasks",
    )
    level = models.PositiveIntegerField(default=1, db_index=True)
    is_done = models.BooleanField(default=False, db_index=True)
    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        db_index=True,
        related_name="tasks",
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        default=None,
        related_name="assigned_tasks",
    )

    def __str__(self):
        return f"{self.pk}-{self.title}"

    def save(self, *args, **kwargs):
        # detect if task was marked as done
        was_done_before = False
        if self.pk:
            old = (
                Task.objects.filter(pk=self.pk)
                .values_list("is_done", flat=True)
                .first()
            )
            was_done_before = old

        super().save(*args, **kwargs)

        # if just changed to done, update all children recursively
        if not was_done_before and self.is_done:
            self.mark_children_done()

        if not self.is_done:
            self.mark_parent_not_done()

    def mark_children_done(self):
        """Recursively mark all nested children as done."""
        subtasks = self.subtasks.all()
        if not subtasks.exists():
            return

        with transaction.atomic():
            for subtask in subtasks:
                if not subtask.is_done:
                    subtask.is_done = True
                    subtask.save()

    def mark_parent_not_done(self):
        parent: Task = self.parent_task
        if parent and parent.is_done:
            parent.is_done = False
            parent.save()
