from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.core.tasks.models import TaskStatus
from taskero_be.users.models import User
from rest_framework import serializers


class MemberWiseWorkloadSerializer(BaseModelSerializer[User]):
    workload = serializers.FloatField(read_only=True)
    task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "email", "workload", "task_count"]

class StatusWiseTaskCountSerializer(BaseModelSerializer[TaskStatus]):
    task_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskStatus
        fields = ["id", "title", "task_count"]
