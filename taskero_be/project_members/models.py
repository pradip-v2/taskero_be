from django.db import models

from taskero_be.core.models import BaseModel
from taskero_be.projects.models import Project
from taskero_be.users.models import User


class ProjectMember(BaseModel):
    project = models.ForeignKey[Project](
        Project,
        on_delete=models.CASCADE,
        related_name="project_members",
    )
    member = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        related_name="project_members",
    )

    def __str__(self):
        return f"{self.pk}-{self.member.name}"
