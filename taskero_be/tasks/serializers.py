from rest_framework import serializers

from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.core.tasks.serializers import TaskStatusSerializer
from taskero_be.projects.serializers import ProjectRelationShortSerializer
from taskero_be.tasks.models import Task
from taskero_be.users.api.serializers import UserRelationShortSerializer


class TaskSerializer(BaseModelSerializer[Task]):
    project_data = ProjectRelationShortSerializer(
        source="project",
        read_only=True,
        default=None,
    )
    assignee_data = UserRelationShortSerializer(
        source="assignee",
        read_only=True,
        default=None,
    )
    subtasks_count = serializers.IntegerField(read_only=True, default=0)
    status_data = TaskStatusSerializer(
        source="status",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Task
        fields = serializers.ALL_FIELDS


class TaskDetailSerializer(TaskSerializer):
    subtasks_data = TaskSerializer(
        source="subtasks",
        many=True,
        read_only=True,
        default=[],
    )
    subtasks_count = None

    class Meta:
        model = Task
        fields = serializers.ALL_FIELDS
